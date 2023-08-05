from asyncio import Semaphore
from naas.types import (
    t_delete,
    t_add,
    t_skip,
    t_update,
    t_error,
    t_start,
    t_notebook,
    t_asset,
    t_dependency,
    t_scheduler,
    t_list,
)
from .env_var import n_env
import pandas as pd
import datetime
import errno
import json
import os
import uuid
from sanic.exceptions import ServerError


filters = [t_notebook, t_asset, t_dependency, t_scheduler]
filters_api = [t_notebook, t_asset]


class Jobs:
    __storage_sem = None
    __df = None
    __logger = None
    __naas_folder = ".naas"
    __json_name = "jobs.json"

    def __init__(self, logger, clean=False, init_data=[]):
        self.__path_naas_files = os.path.join(n_env.server_root, self.__naas_folder)
        self.__json_secrets_path = os.path.join(
            self.__path_naas_files, self.__json_name
        )
        self.__storage_sem = Semaphore(1)
        self.__logger = logger
        if not os.path.exists(self.__path_naas_files):
            try:
                print("Init Naas folder Jobs")
                os.makedirs(self.__path_naas_files)
            except OSError as exc:  # Guard against race condition
                print("__path_naas_files", self.__path_naas_files)
                if exc.errno != errno.EEXIST:
                    raise
            except Exception as e:
                print("Exception", e)
        if not os.path.exists(self.__json_secrets_path) or clean:
            uid = str(uuid.uuid4())
            try:
                print("Init Job Storage", self.__json_secrets_path)
                self.__save_to_file(uid, init_data)
                self.__df = None
            except Exception as e:
                print("Exception", e)
                self.__logger.error(
                    {
                        "id": uid,
                        "type": "init_job_storage",
                        "filepath": self.__json_secrets_path,
                        "status": "error",
                        "error": str(e),
                    }
                )
        else:
            uid = str(uuid.uuid4())
            self.__df = self.__get_save_from_file(uid)
            self.__cleanup_jobs()
        if self.__df is None or len(self.__df) == 0:
            self.__df = pd.DataFrame(
                columns=[
                    "id",
                    "type",
                    "value",
                    "path",
                    "status",
                    "params",
                    "lastUpdate",
                    "lastRun",
                    "nbRun",
                    "totalRun",
                ]
            )

    def __cleanup_jobs(self):
        if len(self.__df) > 0:
            self.__df = self.__df[self.__df.type.isin(filters)]
            self.__dedup_jobs()

    def __dedup_jobs(self):
        new_df = self.__df[
            (self.__df.type != t_notebook) & (self.__df.type != t_asset)
        ].to_dict("records")
        cur_notebook = self.__df[self.__df.type == t_notebook]
        cur_asset = self.__df[self.__df.type == t_asset]
        cur_asset = cur_asset.drop_duplicates(subset=["value"]).to_dict("records")
        cur_notebook = cur_notebook.drop_duplicates(subset=["value"]).to_dict("records")
        self.__df = pd.DataFrame([*new_df, *cur_asset, *cur_notebook])
        self.__df = self.__df.reset_index(drop=True)

    def __get_save_from_file(self, uid):
        data = []
        try:
            with open(self.__json_secrets_path, "r") as f:
                data = json.load(f)
                f.close()
        except Exception as err:
            self.__logger.error(
                {
                    "id": str(uid),
                    "type": "__get_save_from_file",
                    "status": "exception",
                    "filepath": self.__json_secrets_path,
                    "error": str(err),
                }
            )
        return pd.DataFrame(data).reset_index(drop=True)

    def __save_to_file(self, uid, data):
        try:
            with open(self.__json_secrets_path, "w+") as f:
                f.write(
                    json.dumps(data, sort_keys=True, indent=4).replace("NaN", "null")
                )
                f.close()
        except Exception as err:
            print(f"==> Cannot save {uid} \n\n", err)
            self.__logger.error(
                {
                    "id": str(uid),
                    "type": "__save_to_file",
                    "status": "exception",
                    "filepath": self.__json_secrets_path,
                    "error": str(err),
                }
            )

    async def find_by_value(self, uid, value, target_type):
        res = None
        async with self.__storage_sem:
            try:
                if len(self.__df) > 0:
                    cur_jobs = self.__df[
                        (self.__df.type == target_type) & (self.__df.value == value)
                    ]
                    cur_job = cur_jobs.to_dict("records")
                    if len(cur_job) > 0:
                        res = cur_job[0]
            except Exception as e:
                print("find_by_value", e)
            return res

    async def find_by_path(self, uid, filepath, target_type=None):
        res = None
        async with self.__storage_sem:
            try:
                if len(self.__df) > 0:
                    if target_type:
                        cur_jobs = self.__df[
                            (self.__df.type == target_type)
                            & (self.__df.path == filepath)
                        ]
                    else:
                        cur_jobs = self.__df[(self.__df.path == filepath)]
                    cur_job = cur_jobs.to_dict("records")
                    if len(cur_job) > 0:
                        res = cur_job[0]
            except Exception as e:
                print("find_by_path", e)
            return res

    async def is_running(self, uid, notebook_filepath, target_type):
        res = False
        try:
            cur_job = await self.find_by_path(uid, notebook_filepath, target_type)
            if cur_job:
                status = cur_job.get("status", None)
                if status and status == t_start:
                    res = True
        except Exception as e:
            print("is_running", e)
        return res

    def __match_clear(self, cur_filename, filename, clear_all):
        if clear_all and cur_filename.endwith(filename):
            return True
        elif not clear_all and cur_filename == filename:
            return True
        else:
            return False

    def clear_file(self, uid, path, histo):
        # possible format
        # histo_filename
        # out_filename
        # histo_out_filename
        filename = None
        clear_all = False
        if histo and histo == "all":
            clear_all = True
        elif histo:
            filename = f"{histo}_{os.path.basename(path)}"
        else:
            filename = os.path.basename(path)
        removed = []
        dirname = os.path.dirname(path)
        if os.path.exists(path):
            for ffile in os.listdir(dirname):
                if self.__match_clear(ffile, filename, clear_all):
                    tmp_path = os.path.join(dirname, ffile)
                    removed.append(tmp_path)
                    self.__logger.info(
                        {
                            "id": uid,
                            "filename": filename,
                            "histo": histo,
                            "type": "clear_file",
                            "status": t_delete,
                            "filepath": path,
                        }
                    )
                    os.remove(tmp_path)
        return removed

    def list_files(self, uid, path, filetype, output=False):
        d = []
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        if output:
            filename = f"output_{filetype}_{filename}"
        else:
            filename = f"{filetype}_{filename}"
        for ffile in os.listdir(dirname):
            if ffile.endswith(filename):
                histo = ffile.split("_")[0]
                tmp_path = os.path.join(dirname, ffile)
                d.append({"timestamp": histo, "filepath": tmp_path})
        self.__logger.info(
            {
                "id": uid,
                "type": "clear_file",
                "filename": filename,
                "status": t_list,
                "filepath": path,
            }
        )
        return d

    async def list(self, uid, as_df=False):
        data = []
        try:
            async with self.__storage_sem:
                if as_df:
                    data = self.__df
                else:
                    data = self.__df.to_dict("records")
        except Exception as e:
            print("list", e)
        return data

    def __delete(self, cur_elem, uid, path, target_type, value, params):
        try:
            self.__logger.info(
                {
                    "id": uid,
                    "type": target_type,
                    "value": value,
                    "status": t_delete,
                    "filepath": path,
                    "params": params,
                }
            )
            print("drop ==> ", cur_elem.index)
            self.__df = self.__df.drop(cur_elem.index)
            return t_delete
        except Exception as e:
            print("delete", e)
            return t_error

    def __add(self, uid, path, target_type, value, params, run_time):
        try:
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            self.__logger.info(
                {
                    "id": uid,
                    "type": target_type,
                    "value": value,
                    "status": t_add,
                    "filepath": path,
                    "params": params,
                }
            )
            new_row = {
                "id": uid,
                "type": target_type,
                "value": value,
                "status": t_add,
                "path": path,
                "params": params,
                "nbRun": 1 if run_time > 0 else 0,
                "lastRun": run_time,
                "totalRun": run_time,
                "lastUpdate": dt_string,
            }
            cur_df = self.__df.to_dict("records")
            if len(self.__df) > 0:
                self.__df = pd.DataFrame([*cur_df, new_row])
            else:
                self.__df = pd.DataFrame([new_row])
            return t_add
        except Exception as e:
            print("add", e)
            return t_error

    def __clean_dup(self):
        self.__df = self.__df.drop_duplicates(subset=["type", "value"])

    def __update(
        self, cur_elem, uid, path, target_type, value, params, status, run_time
    ):
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        self.__logger.info(
            {
                "id": uid,
                "type": target_type,
                "value": value,
                "status": t_update,
                "filepath": path,
                "params": params,
            }
        )
        index = cur_elem.index[0]
        self.__df.at[index, "id"] = uid
        self.__df.at[index, "status"] = status
        self.__df.at[index, "value"] = value
        self.__df.at[index, "params"] = params
        self.__df.at[index, "lastUpdate"] = dt_string
        if run_time > 0 and status != t_add:
            self.__df.at[index, "nbRun"] = self.__df.at[index, "nbRun"] + 1
            self.__df.at[index, "lastRun"] = run_time
            total_run = float(self.__df.at[index, "totalRun"])
            self.__df.at[index, "totalRun"] = run_time + total_run
            return t_update
        elif status == t_add:
            self.__df.at[index, "nbRun"] = 0
            self.__df.at[index, "lastRun"] = 0
            self.__df.at[index, "totalRun"] = 0
            return t_add
        else:
            return t_skip

    async def update(self, uid, path, target_type, value, params, status, run_time=0):
        data = None
        res = t_error
        async with self.__storage_sem:
            try:
                self.__clean_dup()
                cur_elem = self.__df.query(
                    f'type == "{target_type}" and path == "{path}"'
                )
                if len(cur_elem) == 1 and status == t_delete:
                    res = self.__delete(cur_elem, uid, path, target_type, value, params)
                elif len(cur_elem) == 1:
                    res = self.__update(
                        cur_elem,
                        uid,
                        path,
                        target_type,
                        value,
                        params,
                        status,
                        run_time,
                    )
                elif len(cur_elem) == 0 and status == t_add:
                    res = self.__add(uid, path, target_type, value, params, run_time)
                else:
                    res = t_skip
                if res == t_error:
                    raise ServerError(
                        {
                            "status": "error",
                            "id": uid,
                            "data": [],
                            "error": "unknow error",
                        },
                        status_code=500,
                    )
                data = self.__df.to_dict("records")
                self.__save_to_file(uid, data)
                return {"id": uid, "status": res, "data": data}
            except Exception as e:
                print("cannot update", e)
                self.__logger.error(
                    {
                        "id": uid,
                        "type": target_type,
                        "value": value,
                        "status": t_error,
                        "filepath": path,
                        "params": params,
                        "error": str(e),
                    }
                )
                raise ServerError(
                    {"status": "error", "id": uid, "data": [], "error": str(e)},
                    status_code=500,
                )
