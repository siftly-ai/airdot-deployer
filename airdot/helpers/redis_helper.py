import redis
import json
from airdot.helpers.general_helpers import get_datetime


class redis_helper:
    def __init__(self, host, port, db=None):
        self.host = host
        self.port = port
        self.db = db
        self.redis = redis.Redis(host=self.host, port=self.port, db=self.db)

    def set_key(self, key, value):
        self.redis.set(key, value)

    def get_key(self, key):
        return self.redis.get(key)

    def delete_key(self, key):
        self.redis.delete(key)

    def get_keys(self, pattern):
        return self.redis.keys(pattern)

    def increment_key(self, key):
        self.redis.incr(key)

    def decrement_key(self, key):
        self.redis.decr(key)

    def set_user_function(
        self, id, deploy_dict, function_curl_req, object_refresh=False
    ):
        user_function = self.get_key(id)
        if user_function is not None:  # for a old deployment
            user_function = json.loads(user_function)
            user_function[deploy_dict["name"]]["curl"] = function_curl_req
            user_function[deploy_dict["name"]]["version"] = (
                user_function[deploy_dict["name"]]["version"] + 1
                if not (object_refresh)
                else user_function[deploy_dict["name"]]["version"]
            )
            user_function[deploy_dict["name"]]["data_files"][get_datetime()] = (
                "" if deploy_dict["data_files"] is None else deploy_dict["data_files"]
            )
            user_function[deploy_dict["name"]]["metadata"] = {
                "python_version": deploy_dict["python_version"]
                if not (object_refresh)
                else user_function[deploy_dict["name"]]["metadata"]["python_version"],
                "arg_types": deploy_dict["arg_types"]
                if not (object_refresh)
                else user_function[deploy_dict["name"]]["metadata"]["arg_types"],
                "arg_names": deploy_dict["arg_names"]
                if not (object_refresh)
                else user_function[deploy_dict["name"]]["metadata"]["arg_names"],
            }
        else:
            user_function = dict()
            user_function[deploy_dict["name"]] = {
                "curl": function_curl_req,
                "version": 1,
                "data_files": {
                    get_datetime(): ""
                    if deploy_dict["data_files"] is None
                    else deploy_dict["data_files"]
                },
                "metadata": {
                    "python_version": deploy_dict["python_version"],
                    "arg_types": deploy_dict["arg_types"],
                    "arg_names": deploy_dict["arg_names"],
                },
            }
        try:
            status = self.set_key(
                id,
                json.dumps(user_function),
            )
            return status
        except Exception as e:
            return None
