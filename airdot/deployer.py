import json
import requests
import docker
import shutil
import logging
from time import sleep
from docker.errors import APIError
from typing import cast, Union, Callable, Any, Dict, List, Optional
from airdot.helpers.version_helpers import get_python_default_version
from airdot.helpers.pkg_helpers import get_environment_pkgs, get_pip_list
from airdot.helpers.runtime_helper import get_function_properties
from airdot.helpers.template_helpers import make_soruce_file
from airdot.helpers.general_helpers import get_name, get_difference
from airdot.helpers.data_object_helpers import (
    make_and_upload_data_files,
    upload_runtime_object,
)
from airdot.collection.collections import authentication
from tabulate import tabulate
from airdot.helpers.authentication import (
    user_login,
    verify_user,
    get_user_function,
    get_function_status,
    get_gcs_signed_token,
    push_refreshed_objects,
)
from airdot import URL, VERIFY
from airdot.helpers.docker_helper import docker_helper
from airdot.helpers.redis_helper import redis_helper
from airdot.helpers.network_helper import find_available_port

auth_ = authentication()
# python custom imports
log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)


class Deployer:
    def __init__(
        self,
        minio_endpoint: str = "http://127.0.0.1:9000",
        redis_endpoint: str = "localhost:6379",
        local_deployment=True,
    ) -> None:
        self.docker_client = docker_helper()
        self.minio_endpoint = minio_endpoint
        self.redis_endpoint = redis_endpoint
        self.local_deployment = local_deployment
        self.redis_helper_obj = redis_helper(
            host=self.redis_endpoint.split(":")[0],
            port=self.redis_endpoint.split(":")[1],
        )
        if local_deployment:
            self.minio_network = "minio-network"

    def _perform_user_login(self):
        login_uri = user_login(auth_=auth_)
        if login_uri is None:
            print("login failed please try again")
            return False
        try_auth = 50
        while not (self._is_user_authenticated()) and try_auth > 0:
            sleep(1)
            try_auth -= 1
            continue
        if self._is_user_authenticated(True):
            self.user_login = True
            return self.user_login
        self.user_login = False
        return self.user_login

    def _is_user_authenticated(self, print_status=False):
        if auth_.refresh_token is not None and verify_user(auth_=auth_):
            if print_status:
                print("User authenticated.")
            return True
        return False

    def build_deployment(
        self,
        func: Callable,
        name: Optional[str] = None,
        python_version: Optional[str] = None,
        python_packages: Optional[List[str]] = None,
        system_packages: Optional[List[str]] = None,
    ):
        data_files, dir_id = None, None
        if callable(func):
            python_version = get_python_default_version(python_version)
            env_python_packages = get_environment_pkgs(
                python_packages, func.__globals__
            )
            if python_packages is not None:
                env_python_packages = env_python_packages + python_packages
            func_props = get_function_properties(func, env_python_packages)
            name = get_name(name)
            data_files = make_and_upload_data_files(
                bucket_id=func_props.name.replace("_", "-"),
                open_id=dir_id,
                py_state=func_props,
                endpoint=self.minio_endpoint,
            )  # uploading of data objects.
        elif (
            hasattr(func, "__module__")
            and "sklearn" in func.__module__
            and hasattr(func, "predict")
        ):
            pass
        else:
            raise Exception("Passed object is not callable")

        source_file = make_soruce_file(
            dir=dir_id, pyProps=func_props, source_file_name=name
        )
        return {
            "source_file": source_file.as_dict(),
            "value_files": {},
            "name": func_props.name,
            "data_files": data_files,
            "module": name,
            "arg_names": func_props.arg_names,
            "arg_types": func_props.arg_types,
            "requirements_txt": "\n".join(env_python_packages),
            "python_version": python_version,
            "system_packages": None,  # need to see this
            "dockerRun": None,  # need to build this
        }

    def _list_to_json(self, cld_function_string):
        return dict(
            line.strip().split(":", 1)
            for line in cld_function_string.split("\n")
            if ":" in line
        )

    def _build_url(self, json_string, deploy_dict):
        if json_string is None:
            logging.error("failed to deploy. please try again")
        json_value = self._list_to_json(json_string)
        url = json_value["url"]
        print("Generating Curl request")
        data_dict = {}
        if len(deploy_dict["arg_names"]) > 0:
            for arg_name in deploy_dict["arg_names"]:
                data_dict[arg_name] = "<value-for-argument>"
        curl = f"curl -XPOST {url} -d '{json.dumps(data_dict)}' -H 'Content-Type: application/json' "
        return curl

    def _run_function(self, port):
        try:
            self.image, _ = self.docker_client.create_docker_runtime(
                deploy_dict=self.deploy_dict
            )
            image_name = self.deploy_dict["name"]
            print(f"docker image {image_name} successfully built")
            self.container = self.docker_client.run_container(
                self.image,
                detach=True,
                ports={f"{8080}/tcp": port},
                network=self.minio_network,
            )
            return True
        except Exception as e:
            logging.error(f"{e}")
            return False

    def restart(self, function_id):
        container_id = self.docker_client.get_container_id(function_id)
        self.docker_client.restart_container(container_id=container_id)

    def stop(self, image_name):
        try:
            container_id = self.docker_client.get_container_id(image_name=image_name)
            container_status = self.docker_client.kill_container(
                container_id=container_id
            )
            if container_status:
                self.docker_client.delete_container(container_id=container_id)
                print("deployment killed successfully")
        except APIError as e:
            print(f"{e}")

    def update_redis(self, function_curl, object_refresh=False):
        self.redis_helper_obj.set_user_function(
            self.deploy_dict["name"],
            self.deploy_dict,
            function_curl_req=function_curl,
            object_refresh=object_refresh,
        )

    def run(
        self,
        func: Callable,
        name: Optional[str] = None,
        python_version: Optional[str] = None,
        python_packages: Optional[List[str]] = None,
        system_packages: Optional[List[str]] = None,
    ):

        print("deployment started")
        self.deploy_dict = self.build_deployment(
            func=func,
            name=name,
            python_packages=python_packages,
            python_version=python_version,
            system_packages=system_packages,
        )
        # prepare docker environment
        # print(f"Deploying {self.deploy_dict['name']} it may take couple of minutes")
        if self.local_deployment:
            port = find_available_port(8000)
            print(f"deploying on port: {port}")
            function_status = self._run_function(port)
        else:
            pass

        if function_status:
            if self.local_deployment:
                url = f"http://127.0.0.1:{port}"
                function_curl = self.build_function_url(url=url)
                print("deployment ready, access using the curl command below")
                print(function_curl)
                self.update_redis(function_curl)
        else:
            print("failed to run function. Please try again.")

    def update_objects(self, object, function_id):
        data_files: Dict[str, str] = {}
        if (
            isinstance(object, list)
            and len(object) > 0
            and isinstance(object[0], tuple)
        ):
            for item in object:
                nName = item[0]
                nVal = item[1]
                data_files[f"{nName}.pkl"] = upload_runtime_object(
                    function_id.replace("_", "-"),
                    None,
                    nVal,
                    nName,
                    endpoint=self.minio_endpoint,
                )
            json_dict = {
                "data_files": data_files,
                "function_id": function_id,
                "auth_session_token": auth_.refresh_token,
            }
            status = self.restart(function_id)
            if status is not None:
                return status
        elif isinstance(object, tuple):
            nName = object[0]
            nVal = object[1]
            data_files[f"{nName}.pkl"] = upload_runtime_object(
                function_id.replace("_", "-"),
                None,
                nVal,
                nName,
                endpoint=self.minio_endpoint,
            )
            json_dict = {
                "data_files": data_files,
                "name": function_id,
                "auth_session_token": auth_.refresh_token,
            }
            status = self.restart(function_id)
            if status is not None:
                return status
        else:
            print("Please pass object tuple or list of tuples")

    def _check_function_status(self, deploy_dict):
        payload = {
            "auth_session_token": deploy_dict["auth_session_token"],
            "name": deploy_dict["name"],
        }

        def function_status(payload):
            status = get_function_status(payload=payload)
            if status is not None and json.loads(status)["status"] == "DONE":
                return True
            else:
                return False

        try_check_function_status = 10
        function_status_flag = function_status(payload=payload)
        while not (function_status_flag) and try_check_function_status > 0:
            function_status_flag = function_status(payload=payload)
            try_check_function_status -= 1
            sleep(50)
            continue
        function_status_flag = function_status(payload=payload)
        if function_status_flag:
            return json.loads(get_function_status(payload=payload))
        else:
            return None

    def build_function_url(self, url):
        if url is None:
            print("failed to generate url")
            exit(1)
        url = url
        data_dict = {}
        if len(self.deploy_dict["arg_names"]) > 0:
            for arg_name in self.deploy_dict["arg_names"]:
                data_dict[arg_name] = "<value-for-argument>"
        curl = f"curl -XPOST {url} -H 'Content-Type: application/json' -d '{json.dumps(data_dict)}'  "
        return curl

    def generate_arg_list(self, function_request):
        arg_list = []
        if len(function_request["metadata"]["arg_names"]) > 0:
            for arg_name in function_request["metadata"]["arg_names"]:
                arg_list.append(f"{arg_name}")
            arg_list = arg_list if len(arg_list) > 0 else ["None args defined"]
            return arg_list

    def data_objects_list(self, function_request):
        data_obj_keys = list(function_request["data_files"].keys())
        data_objects_list = []
        for key in data_obj_keys:
            update_keys = list(function_request["data_files"][key].keys())
            for update_key in update_keys:
                data_objects_list.append(
                    f"name {update_key} update time {key.replace('$', ' ')}"
                )
        data_objects_list = (
            data_objects_list
            if len(data_objects_list) > 0
            else ["None data objects found"]
        )
        return data_objects_list

    def list_deployments(self):
        user_functions = self.redis_helper_obj.get_keys("*")
        if user_functions is not None:
            keys = ["deployment-name", "args", "data-objects"]
            function_names = [value.decode() for value in user_functions]
            for function_name in function_names:
                table = []
                json_value = json.loads(self.redis_helper_obj.get_key(function_name))
                curl_request = json_value[function_name]["curl"]
                table.append(
                    [
                        function_name,
                        "\n".join(self.generate_arg_list(json_value[function_name])),
                        "\n".join(self.data_objects_list(json_value[function_name])),
                    ]
                )
                print(f"curl-request {curl_request}")
                print(tabulate(table, keys, "grid"))
