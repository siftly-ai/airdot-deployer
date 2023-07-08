from pydantic import BaseModel
from typing_extensions import Literal
from typing import Optional
from airdot.data_models.seldon_model import SeldonConfiguration
from airdot.data_models.kserve_model import KServe


class Deployment(BaseModel):
    deployment_type: Literal["seldon", "kserve", "local"]
    bucket_type: Optional[str] = None,
    image_uri: Optional[str] = None
    seldon_configuration: Optional[SeldonConfiguration] = {
        'apiVersion': 'machinelearning.seldon.io/v1',
        'kind': 'SeldonDeployment',
        'metadata': {
            'name':'seldon_model'
        },
        'specs':{
            "name": "None",
            "predictors": {
                "componentSpecs": {
                    "specs": {
                        "container": {
                            "name": "None",
                            "image": "None",
                            "imagePullPolicy": "ifNotPresent",
                            "resources": {"requests": {"cpu": "1", "memory": "1M"}},
                        }
                    }
                },
                'graph':{
                    'name':'seldon',
                }
            },
        },
        'name':'default',
        'replicas':1
    }
    kserve_configuration: Optional[KServe]
