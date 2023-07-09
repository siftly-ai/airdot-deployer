import subprocess


def get_s2i_environment(name):
    contents = [
        f"MODEL_NAME={name}",
        "API_TYPE=REST",
        "SERVICE_TYPE=MODEL",
        "PERSISTENCE=0",
    ]
    return "\n".join(contents)


class s2i_python_helper:
    def __init__(self, base_image, builder_image):
        self.base_image = base_image
        self.builder_image = builder_image

    def build_image(self, source_path):
        """
        Build a container image using S2I.

        :param source_path: The path to the source code directory.
        :param image_name: The name of the container image to be built.
        """
        command = [
            "s2i",
            "build",
            source_path,
            self.base_image,
            self.builder_image,
        ]

        subprocess.run(command, check=True)

    def build_and_push_image(
        self, source_path, registry_url=None, username=None, password=None
    ):
        """
        Build a container image using S2I and push it to a container registry.

        :param source_path: The path to the source code directory.
        :param image_name: The name of the container image to be built.
        :param registry_url: The URL of the container registry to push the image to.
        :param username: Optional username for the container registry.
        :param password: Optional password for the container registry.
        """
        self.build_image(source_path)

        if username and password:
            docker_login_command = [
                "docker",
                "login",
                registry_url,
                "--username",
                username,
                "--password",
                password,
            ]
            subprocess.run(docker_login_command, check=True)

        # docker_tag_command = [
        #     "docker",
        #     "tag",
        #     f"{self.builder_image}",
        # ]
        # subprocess.run(docker_tag_command, check=True)

        docker_push_command = ["docker", "push", f"{self.builder_image}"]
        subprocess.run(docker_push_command, check=True)
