from airdot.data_models.deployment import Deployment


class seldon_helpers(object):
    def __init__(self, deployment_configuration) -> None:
        if deployment_configuration is None:
            raise TypeError(
                "failed to build seldon deployment no deployment configuration is provided"
            )

        self.seldon_configuration = Deployment(**deployment_configuration).dict()['seldon_configuration']

    def create_seldon_configuration(self, deploy_dict, image_uri):
        if self.seldon_configuration['apiVersion'] == "None":
            self.seldon_configuration['apiVersion'] = "machinelearning.seldon.io/v1"
            self.seldon_configuration['metadata']['name'] = f"{deploy_dict['name'].replace('_','-')}"
            self.seldon_configuration['metadata']['namespace'] = f"{deploy_dict['name'].replace('_','-')}"
            self.seldon_configuration['spec']['predictors'][0]['componentSpecs'][0]['spec']['containers'][0]['name'] = f"{deploy_dict['name'].replace('_','-')}"
            self.seldon_configuration['spec']['predictors'][0]['componentSpecs'][0]['spec']['containers'][0]['image'] = f"{image_uri}"
            self.seldon_configuration['spec']['predictors'][0]['graph']['name'] = f"{deploy_dict['name'].replace('_','-')}"
            self.seldon_configuration['spec']['predictors'][0]['name'] = f"{deploy_dict['name'].replace('_','-')}"
            self.seldon_configuration['spec']['predictors'][0]['replicas'] = 1
        return self.seldon_configuration
