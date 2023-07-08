import os
import json
import yaml
import random
import string
from airdot.helpers.template_helpers import get_docker_template
from airdot.helpers.s2i_helper import get_s2i_environment

DEFAULT_PKG_LIST = ["Flask", "gunicorn", "boto3"]


class content_helper:
    def __init__(
        self, deploy_dict=None, deployment_type=None, seldon_configuration=None
    ) -> str:
        self.deploy_dict = deploy_dict
        self.deployment_type = deployment_type
        self.seldon_configuration = seldon_configuration

    def write_contents(self):
        try:
            deployment_path = self.create_tmp_directory()
            if self.deployment_type == "test":
                # write python file
                user_contents = self.deploy_dict["source_file"]["user_contents"]
                file_name = self.deploy_dict["source_file"]["user_name"]
                py_path = os.path.join(deployment_path, file_name)
                self.write_python_file(
                    py_path, "\n".join(user_contents.split("\n")) + "\n"
                )
                # write docker file
                requirements_file_content = self.get_custom_requirements(
                    self.deploy_dict["requirements_txt"], DEFAULT_PKG_LIST
                )
                docker_template = get_docker_template(requirements_file_content, self.deploy_dict["source_file"]["user_name"].split('.')[0])
                dockerfile_path = os.path.join(deployment_path, "Dockerfile")
                self.write_custom_file(dockerfile_path, "\n".join(docker_template))
                return deployment_path

            elif self.deployment_type == "seldon":
                # write user python file
                user_contents = self.deploy_dict["source_file"]["user_contents"]
                file_name = self.deploy_dict["source_file"]["user_name"]
                py_path = os.path.join(deployment_path, file_name)
                self.write_python_file(
                    py_path, "\n".join(user_contents.split("\n")) + "\n"
                )

                # write seldon contents file
                user_contents = self.deploy_dict["source_file"]["seldon_contents"]
                file_name = self.deploy_dict["source_file"]["seldon_name"]
                py_path = os.path.join(deployment_path, file_name)
                self.write_python_file(
                    py_path, "\n".join(user_contents.split("\n")) + "\n"
                )

                # .s2i/env file
                os.mkdir(os.path.join(deployment_path, ".s2i"))
                s2i_path = os.path.join(deployment_path, ".s2i/environment")
                self.write_custom_file(
                    s2i_path, get_s2i_environment(self.deploy_dict["name"])
                )
                # write kubect yaml file
                yaml_path = os.path.join(deployment_path, "seldon_model.json")
                self.write_json_file(yaml_path, self.seldon_configuration)
                return deployment_path

            elif self.deployment_type == "kserve":

                pass
        except Exception as e:
            print(f"{e}")

    def id_generator(self, size=4, chars=string.ascii_lowercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    def get_custom_requirements(self, requirements_txt, default_path: str = ""):
        pkg_list = requirements_txt.split("\n")
        return " ".join(pkg_list + default_path)

    def create_tmp_directory(self):
        try:
            dir = self.id_generator(size=9)
            path = f"/tmp/{dir}"
            os.mkdir(path)
            return path
        except Exception as e:
            print(f"failed to create temporary directory {e}")
            return None

    def write_file(self, file_path, content):
        """
        Write content to a file.

        :param file_path: The path of the file to be written.
        :param content: The content to write to the file.
        """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w") as file:
            file.write(content)

    def write_python_file(self, file_path, content):
        """
        Write content to a Python (.py) file.

        :param file_path: The path of the Python file to be written.
        :param content: The content to write to the file.
        """
        if not file_path.endswith(".py"):
            file_path += ".py"

        self.write_file(file_path, content)

    def write_text_file(self, file_path, content):
        """
        Write content to a text (.txt) file.

        :param file_path: The path of the text file to be written.
        :param content: The content to write to the file.
        """
        if not file_path.endswith(".txt"):
            file_path += ".txt"

        self.write_file(file_path, content)

    def write_json_file(self, file_path, data):
        """
        Write JSON data to a JSON (.json) file.

        :param file_path: The path of the JSON file to be written.
        :param data: The JSON data to write to the file.
        """
        if not file_path.endswith(".json"):
            file_path += ".json"

        json_content = json.dumps(data, indent=4)
        self.write_file(file_path, json_content)

    def write_yaml_file(self, file_path, data):
        """
        Write YAML data to a YAML (.yaml) file.

        :param file_path: The path of the YAML file to be written.
        :param data: The YAML data to write to the file.
        """
        if not file_path.endswith(".yaml"):
            file_path += ".yaml"

        yaml_content = yaml.dump(data, sort_keys=False)
        self.write_file(file_path, yaml_content)

    def write_custom_file(self, file_path, content):
        """
        Write content to a custom file with no extension.

        :param file_path: The path of the custom file to be written.
        :param content: The content to write to the file.
        """
        self.write_file(file_path, content)
