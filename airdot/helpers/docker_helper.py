import os
import string
import random
import docker
from airdot.helpers.template_helpers import get_docker_template

DEFAULT_PKG_LIST = ["Flask", "gunicorn", "boto3"]


class docker_helper:
    def __init__(self):
        self.client = docker.from_env()

    def run_container(
        self,
        image_name,
        command=None,
        detach=True,
        remove=True,
        ports=None,
        network=None,
    ):
        try:
            container = self.client.containers.run(
                image_name,
                command,
                detach=detach,
                remove=remove,
                ports=ports,
                network=network,
            )
            return container
        except docker.errors.ImageNotFound:
            print(f"Error: Image '{image_name}' not found")
        except docker.errors.APIError as e:
            print(f"Error starting container: {e}")

    def get_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            return container.id
        except docker.errors.NotFound:
            print(f"Error: Container '{container_id}' not found")
        except docker.errors.APIError as e:
            print(f"Error getting container ID: {e}")

    def get_container_id(self, image_name):
        container_id = None
        containers = self.client.containers.list(all=True)
        for container in containers:
            if container.image.tags[0].split(":")[0] == image_name:
                container_id = container.id
        return container_id

    def kill_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.kill()
            return True
        except docker.errors.NotFound:
            print(f"Error: Container '{container_id}' not found")
        except docker.errors.APIError as e:
            print(f"Error killing container: {e}")
            return False

    def delete_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.remove()
            return True
        except docker.errors.NotFound:
            print(f"Error: Container '{container_id}' not found")
        except docker.errors.APIError as e:
            print(f"Error deleting container: {e}")
            return False

    def restart_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.restart()
            print(f"Container '{container_id}' restarted successfully")
        except docker.errors.NotFound:
            print(f"Container '{container_id}' not found")

    def create_docker_runtime(self, deploy_dict):
        dir = self.write_user_file(deploy_dict["source_file"])
        custum_req = self.get_custom_requirements(deploy_dict["requirements_txt"])
        success_flag = self.create_custom_docker_file(custum_req, dir)
        if success_flag:
            image, _ = self.client.images.build(
                path=f"/tmp/{dir}/", tag=f"{deploy_dict['name']}"
            )
            return image, dir
        return None, None

    def create_custom_docker_file(self, custum_req, dir):
        try:
            docker_template = get_docker_template(custum_req)
            with open(f"/tmp/{dir}/Dockerfile", "w") as py_file:
                py_file.write("\n".join(docker_template) + "\n")
            return True
        except:
            return False

    def get_custom_requirements(self, requirements_txt):
        pkg_list = requirements_txt.split("\n")
        return " ".join(pkg_list + DEFAULT_PKG_LIST)

    def write_user_file(self, source_file):
        try:
            dir = self.id_generator()
            os.mkdir(f"/tmp/{dir}")
            with open(f"/tmp/{dir}/app.py", "w") as py_file:
                py_file.write("\n".join(source_file["contents"].split("\n")) + "\n")
            return dir
        except:
            return None

    def id_generator(self, size=4, chars=string.ascii_lowercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))
