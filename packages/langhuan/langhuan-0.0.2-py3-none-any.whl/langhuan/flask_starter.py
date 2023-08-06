from .hyperflask import HyperFlask
from .history import History
from .options import Options
from .utility import now_str, now_specific, cleanup_tags,\
    arg_by_key

from flask import Flask, request, jsonify
from flask.templating import render_template
import logging
import json
import pandas as pd
from typing import List, Union, Callable
from pathlib import Path
from uuid import uuid4


def get_root() -> Path:
    return Path(__file__).parent.absolute()


class Progress:
    """
    A project progress handler,
        allowing multiple but limited number of users
        working a the same progress, with limited tags
        per entry of raw data
    """

    def __init__(
        self,
        progress_list: List[int],
        cross_verify_num: int = 1,
        history_length: int = 20,
    ):
        self.progress_list = progress_list
        self.history_length = history_length
        self.v_num = cross_verify_num
        self.ct = 0
        self.depth = dict((i, dict()) for i in range(len(progress_list)))
        self.personal_history = dict()
        self.idx_to_index = dict((v, k) for k, v in enumerate(progress_list))

        self.by_user_wip = dict()

    def __getitem__(self, index: int) -> Union[int, str]:
        return self.progress_list[index]

    def next_id(self, user_id: str) -> Union[int, str]:
        """
        user_id, random generated hex string
        return the next id for dataframe index
        """
        if self.ct >= len(self.progress_list):
            raise StopIteration("Task done")

        if len(self.depth[self.ct]) >= self.v_num:
            self.ct += 1
            return self.next_id(user_id)

        elif len(self.depth[self.ct]) +\
            len(list(filter(
                lambda x: x == self.ct,
                self.by_user_wip.values()))) >= self.v_num:
            self.ct += 1
            return self.next_id(user_id)

        else:
            self.by_user_wip[user_id] = self.ct
            return self.ct

    def tagging(self, data):
        index = data["index"]
        user_id = data["user_id"]
        # recover the pandas index
        self.depth[index][user_id] = data
        self.update_personal(data)
        if user_id in self.by_user_wip:
            del self.by_user_wip[user_id]

    def update_personal(self, data):
        """
        update data to personal history
        """
        user_id = data["user_id"]
        personal_history = self.personal_history.get(user_id)
        if type(personal_history) == list:
            for d in personal_history:
                if data["index"] == d["index"]:
                    personal_history.remove(d)
            personal_history.append(data)
            if len(personal_history) > self.history_length:
                personal_history = personal_history[
                    len(personal_history) - self.history_length:]
        else:
            self.personal_history[user_id] = []
            self.update_personal(data)


class LangHuanBaseTask(Flask):
    task_type = None

    @classmethod
    def from_df(
        cls,
        df: pd.DataFrame,
        text_col: str,
        task_name: str = None,
        options: List[str] = None,
        load_history: bool = False,
        save_frequency: int = 42,
        order_strategy: Union[str, Callable] = "forward_march",
        order_by_column: str = None,
        cross_verify_num: int = 1,
        admin_control: bool = False,
    ):
        """
        Input columns:

        - text_col: str, column name that contains raw data
        - options: List[str] = None, a list of string options
            you don't even have to decide this now, you can input
            None and configure it on /admin page later
        - load_history: bool = False, load the saved history if True
        - task_name: str, name of your task, if not provided
        - cross_verify_num: int = 1, this number decides how many
            people should see to one entry at least
        - admin_control: bool = False, if True you have to
            set adminkey as query string or post data when visit
            admin related sites
        """
        app_name = cls.create_task_name(task_name, cls.task_type)

        logging.getLogger().setLevel(logging.INFO)
        app = cls(
            app_name,
            static_folder=str(get_root()/"static"),
            template_folder=str(get_root()/"templates")
        )

        app.task_history = History(
            app_name,
            load_history=load_history,
            save_frequency=save_frequency,
        )

        app.admin_control = admin_control
        if app.admin_control:
            app.admin_key = str(uuid4())

        if app.admin_control:
            logging.info(
                f"please visit admin page:/admin?adminkey={app.admin_key}")

        app.config['TEMPLATES_AUTO_RELOAD'] = True
        HyperFlask(app)

        app.register(df, text_col, Options(df, options))
        app.create_progress(order_strategy, order_by_column, cross_verify_num)

        if load_history:
            # loading the history to progress
            if len(app.task_history.history) > 0:
                for data in app.task_history.history:
                    app.progress.tagging(data)
        return app

    def forward_march(self, **kwargs) -> List[int]:
        return list(self.df.index)

    def mix_streams(self, *streams):
        if len(streams) == 0:
            return []
        elif len(streams) == 1:
            return list(streams[0])

        min_length = min(list(map(len, streams)))
        combined = []
        for i in range(min_length):
            for stream in streams:
                combined.append(stream[i])

        combined += self.mix_streams(*list(
            stream[min_length:] for stream in streams
            if stream[min_length:] > 0))

        return combined

    def pincer(self, **kwargs) -> List[int]:
        order_by_column = kwargs.get("order_by_column")
        if order_by_column is None:
            raise KeyError(
                "you have to set 'order_by_column' " +
                "when using pincer strategy, " +
                "preferably a score between 0 ~ 1"
            )

        ordered_idx = list(
            self.df.sort_values(by=[order_by_column, ]).index)

        mid_point = len(ordered_idx)//2
        return self.mix_streams(
            ordered_idx[:mid_point], ordered_idx[mid_point:][::-1])

    def trident(self, **kwargs) -> List[int]:
        order_by_column = kwargs.get("order_by_column")
        if order_by_column is None:
            raise KeyError(
                "you have to set 'order_by_column' " +
                "when using trident strategy, " +
                "preferably a score between 0 ~ 1"
            )

        mid_score = self.df[order_by_column].min() +\
            (self.df[order_by_column].max() -
             self.df[order_by_column].min())/2

        sorted_df = self.df.sort_values(by=[order_by_column, ])

        bigger = sorted_df.query(f"{order_by_column}>={mid_score}")
        smaller = sorted_df.query(f"{order_by_column}<{mid_score}")

        bigger_mid_point = len(bigger)//2
        smaller_mid_point = len(smaller)//2

        return self.mix_streams(
            list(bigger.index)[:bigger_mid_point],
            list(bigger.index)[bigger_mid_point:][::-1],
            list(smaller.index)[:smaller_mid_point],
            list(smaller.index)[smaller_mid_point:][::-1],
        )

    def create_progress(
        self,
        order_strategy: str,
        order_by_column: str,
        cross_verify_num: int,
    ) -> List[int]:
        strategy_options = {
            "forward_march": self.forward_march,
            "pincer": self.pincer,
            "trident": self.trident,
        }

        if type(order_strategy) == str:
            assert order_strategy in strategy_options,\
                f"""order_strategy has to be one of
            {list(strategy_options.keys())}"""
            self.progress_list = strategy_options[order_strategy](
                order_by_column=order_by_column)
        else:
            self.progress_list = order_strategy()
        self.progress = Progress(
            self.progress_list, cross_verify_num=cross_verify_num)
        return self.progress_list

    def __repr__(self):
        return f"""{self.__class__.__name__},
        self.run('0.0.0.0', debug=True)"""

    @staticmethod
    def create_task_name(task_name, task_type):
        return task_name if task_name else f"task_{task_type}_{now_str()}"

    def log_skip(self, user_id):
        """
        try to see if the user is working on some other entry
            if do, log the skipped
        """
        if user_id in self.progress.by_user_wip:
            index = self.progress.by_user_wip[user_id]
            logging.info(
                f"user: [{user_id}] skipping {index}")
            self.task_history +\
                dict(
                    index=index,
                    user_id=user_id)
            del self.progress.by_user_wip[user_id]

    def register(
        self,
        df: pd.DataFrame,
        text_col: str,
        options: List[str],
    ) -> None:
        return NotImplementedError(
            "LangHuanBaseTask.register() should be over writen")

    def admin_access(self, f: Callable) -> Callable:
        """
        simple access control
        you can access the GET url by passing query string
            by key: adminkey
        you can access the POST url by passing data
            by key: adminkey

        adminkey can be obtained in console
            when first initiated,
            or print out app.admin_key

        this function is intended to be used as decorator
        """
        def wrapper():
            if self.admin_control:
                admin_key = arg_by_key("adminkey")
                if admin_key is None:
                    return "<h3>please provide adminkey</h3>", 403
                if admin_key == self.admin_key:
                    return f()
                else:
                    return "<h3>'adminkey' not correct</h3>", 403
        wrapper.__name__ = f.__name__
        return wrapper

    def register_functions(self):
        """
        register the custom decorated route functions
        """
        @self.route("/data", methods=["POST", "GET"])
        def raw_data():
            index = arg_by_key("index")
            user_id = arg_by_key("user_id")
            # move on the progress
            if index == -1:
                try:
                    self.log_skip(user_id)
                    index = self.progress.next_id(user_id)
                except StopIteration:
                    return jsonify(dict(done=True))

            # transform range index to dataframe index
            idx = self.progress[index]
            text = cleanup_tags(self.df.loc[idx, self.text_col])
            options = self.options[idx]

            rt = dict(idx=idx, index=index, text=text, options=list(options))

            if user_id in self.progress.depth[index].keys():
                rt.update({"record": self.progress.depth[index][user_id]})

            return jsonify(rt)

        @self.route("/tagging", methods=["POST"])
        def tagging():
            remote_addr = request.remote_addr
            data = json.loads(request.data)
            data.update({
                "remote_addr": remote_addr,
                "now": now_specific(),
                "pandas": self.progress[data["index"]]
            })
            self.progress.tagging(data)
            self.task_history + data
            return jsonify({"index": data["index"]}), 200

        @self.route("/latest", methods=["POST", "GET"])
        def lastest():
            if request.method == "POST":
                data = json.loads(request.data)
                n = data["n"] if "n" in data else 20
            else:
                n = 20
            return jsonify(self.task_history.history[-n:][::-1])

        @self.route("/save_progress", methods=["GET", "POST"])
        def save_progress():
            self.task_history.save_new_history()
            return jsonify(
                {"so_far": self.task_history.history_save_mark}
            )

        @self.route("/monitor", methods=["POST", "GET"])
        def monitor():
            stats = dict(
                total=len(self.progress.progress_list),
                by_user=self.progress.by_user_wip,
                current_id=self.progress.ct,
            )
            return jsonify(stats)

        @self.route("/tagged", methods=["POST", "GET"])
        def tagged_data():
            return jsonify(
                dict((k, v) for k, v in self.progress.depth.items()
                     if len(v) > 0))

        @self.route("/get_options", methods=["POST", "GET"])
        @self.admin_access
        def get_options():
            return jsonify(self.options.known_options)

        @self.route("/stats", methods=["POST", "GET"])
        @self.admin_access
        def get_stats():
            """
            get by user statistics
            """
            user_ids = list(self.progress.personal_history.keys())
            empety = dict(
                entries=[],
                skipped=[],
            )
            by_user = dict((u, empety) for u in user_ids)
            for index, user_entry in self.progress.depth.items():
                for user_id, data in user_entry.items():
                    index = data["index"]
                    by_user[user_id]["entries"].append(index)
                    if "skipped" in data:
                        by_user[user_id]["skipped"].append(index)
            for user_id, v in by_user.items():
                v["entry_ct"] = len(set(v["entries"]))
                v["skip_ct"] = len(set(v["skipped"]))
                del v["entries"]
                del v["skipped"]
            return jsonify(by_user)

        @self.route("/add_option", methods=["POST", "GET"])
        @self.admin_access
        def add_option():
            """
            add a new tagging option
            Input:
            - option: str
            """
            option = arg_by_key("option")
            self.options.add_option(option)
            return jsonify({"option": option})

        @self.route("/delete_option", methods=["POST", "GET"])
        @self.admin_access
        def delete_option():
            """
            delete an existing tagging option
            Input:
            - option: str
            """
            option = arg_by_key("option")
            self.options.delete_option(option)
            return jsonify({"option": option})

        @self.route("/admin")
        @self.admin_access
        def admin():
            """
            The admin page
            """
            return render_template("admin.html")


class NERTask(LangHuanBaseTask):
    """
    NER Task
    """
    task_type = "NER"

    def register(
        self,
        df: pd.DataFrame,
        text_col: Union[List[str], str],
        options: List[str],
    ) -> None:
        self.df = df
        self.text_col = text_col
        self.options = options

        @self.route("/")
        def idx_page():
            # with specific index
            index_qs = arg_by_key("index")
            if index_qs is not None:
                index = index_qs[0]
            else:
                index = -1
            return render_template(
                "ner.html",
                index=index,
            )

        @self.route("/result")
        def download_result():
            """
            return the result as a big json string
            """
            result = dict(
                data=dict((k, list(d for u, d in v.items())) for k, v in
                          self.progress.depth.items() if len(v) > 0),
                text_col=self.text_col,
                options=self.options.known_options,
                admin_control=self.admin_control,
            )
            return jsonify(result)

        @self.route("/personal_history")
        def personal_history():
            user_id = arg_by_key("user_id")
            result = []
            personal_history = self.progress.personal_history.get(user_id)

            if personal_history is None:
                return jsonify([])

            for history in personal_history:
                if "skipped" in history:
                    result.append({
                        "index": history["index"],
                        "time": history["now"],
                        "tags": 0,
                        "skipped": True,
                    })
                else:
                    result.append(
                        {"index": history["index"],
                         "time": history["now"],
                         "tags": len(history["tags"])})

            return jsonify(result[::-1])

        self.register_functions()
