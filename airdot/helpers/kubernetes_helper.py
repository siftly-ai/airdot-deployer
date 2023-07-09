import subprocess
import yaml
from kubernetes import config, client


class k8s:
    def __init__(self):  # Optional: specify the context to use
        self.context = self.get_current_cluster_config()

    def get_current_cluster_config(self):
        try:
            current_context = config.list_kube_config_contexts()[1]["context"]
            return current_context
        except Exception as e:
            print(f"Failed to retrieve cluster configuration: {e}")
            return None

    def apply_kubernetes_resources(self, resource_paths):
        try:
            subprocess.check_call(
                    ["kubectl", "apply", "-f", resource_paths]
                )
            print("Resources applied successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to apply resources: {e}")

    def create_namespace(self, namespace):
        try:
            subprocess.check_call(
                ["kubectl", "create", "namespace", namespace]
            )
            print(f"Namespace '{namespace}' created successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create namespace: {e}")
            return False

    def delete_namespace(self, namespace):
        try:
            subprocess.check_call(
                ["kubectl", "delete", "namespace", namespace, "--context", self.context]
            )
            print(f"Namespace '{namespace}' deleted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to delete namespace: {e}")
