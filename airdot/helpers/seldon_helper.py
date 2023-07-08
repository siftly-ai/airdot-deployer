
class seldon_helpers(object):
    def __init__(self, deployment_configuration) -> None:
        if deployment_configuration is None:
            raise TypeError('failed to build seldon deployment no deployment configuration is provided')
        
    def get_current_cluster_context(self):
        pass