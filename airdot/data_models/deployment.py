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
                "apiVersion": "None",
                "kind": "SeldonDeployment",
                "metadata": {
                    "name": "None",
                    "namespace":"None"
                },
                "spec": {
                    "name": "seldon-test",
                    "predictors": [{
                    "componentSpecs":[{
                        "spec": {
                        "containers": [{
                            "name": "None",
                            "image": "None",
                            "imagePullPolicy": "Always",
                            "resources": {
                            "requests": {
                                "cpu": "1",
                                "memory": "1M"
                            }
                            }
                        }]
                        }
                    }],
                    "graph":{
                        "children":[],
                        "name":"None",
                        "endpoint": {
                            "type":"REST"
                        },
                        "type": "MODEL"
                    },
                    "name":"seldon-test",
                    "replicas":1
                    }]
                }
            }
    kserve_configuration: Optional[KServe]
