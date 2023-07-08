from airdot.data_models.deployment import Deployment


class seldon_helpers(object):
    def __init__(self, deployment_configuration) -> None:
        if deployment_configuration is None:
            raise TypeError(
                "failed to build seldon deployment no deployment configuration is provided"
            )

        self.seldon_configuration = Deployment(**deployment_configuration).dict()['seldon_configuration']

    def create_seldon_configuration(self, deploy_dict, image_uri):
        self.seldon_configuration['metadata']['name'] = f"{deploy_dict['name']}"
        self.seldon_configuration['specs']['predictors']['componentSpecs']['specs']['container']['name'] = f"{deploy_dict['name']}"
        self.seldon_configuration['specs']['predictors']['componentSpecs']['specs']['container']['image'] = f"{image_uri}"
        print(self.seldon_configuration)
        return self.seldon_configuration
