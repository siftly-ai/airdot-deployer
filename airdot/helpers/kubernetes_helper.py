import subprocess
import yaml
from kubernetes import config, client


class KubernetesHelper:
    def __init__(self, context=''):  # Optional: specify the context to use
        config.load_kube_config()

    def get_current_cluster_config(self):
        try:
            current_context = config.list_kube_config_contexts()[1]['context']
            return current_context
        except Exception as e:
            print(f"Failed to retrieve cluster configuration: {e}")
            return None

    def get_current_cluster_config(self):
        try:
            if self.context:
                config = subprocess.check_output(['kubectl', 'config', 'view', '--raw', '--minify', '--context', self.context])
            else:
                config = subprocess.check_output(['kubectl', 'config', 'view', '--raw', '--minify'])
            return yaml.safe_load(config)
        except subprocess.CalledProcessError as e:
            print(f"Failed to retrieve cluster configuration: {e}")
            return None

    def apply_kubernetes_resources(self, resource_paths):
        try:
            for path in resource_paths:
                subprocess.check_call(['kubectl', 'apply', '-f', path, '--context', self.context])
            print("Resources applied successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to apply resources: {e}")

# Example usage:
# helper = KubernetesHelper(context='my-context')
# config = helper.get_current_cluster_config()
# if config:
#     print(f"Current cluster context: {config['current-context']}")
#     # Apply a YAML file
#     helper.apply_kubernetes_resources(['deployment.yaml'])
