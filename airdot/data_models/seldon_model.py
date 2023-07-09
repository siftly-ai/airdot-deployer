from pydantic import BaseModel
from typing_extensions import Literal
from typing import Optional


class SeldonMetadata(BaseModel):
    labels: Optional[dict] = {"app": "seldon"}
    name: Optional[str] = "seldon_app"


class SeldonAnnotations(BaseModel):
    project_name: Optional[str] = "seldon_model"
    deployment_version: Optional[str] = "0"


class SeldonContainer(BaseModel):
    name: str
    imagePullPolicy: Optional[str] = "IfNotPresent"
    resources: Optional[dict] = {"requests": {"cpu": "1", "memory": "1M"}}


class SeldonPodSpecs(BaseModel):
    nodeSepector: Optional[dict]
    containers: Optional[SeldonContainer] = {
        "name": "seldon_container",
        "image": "None",
        "imagePullPolicy": "IfNotPresent",
        "resources": {"requests": {"cpu": "1", "memory": "1M"}},
    }


class SeldonComponentSpecs(BaseModel):
    specs: SeldonPodSpecs


class SeldonSpecs(BaseModel):
    annotations: Optional[SeldonAnnotations]
    name: Optional[str] = "seldon_model"
    predictors: Optional[SeldonComponentSpecs]


class SeldonGraph(BaseModel):
    name: Optional[str] = {"name": "seldon_model"}


class SeldonConfiguration(BaseModel):
    apiVersion: Optional[
        Literal["machinelearning.seldon.io/v1", "machinelearning.seldon.io/v1alpha2"]
    ] = "machinelearning.seldon.io/v1"
    kind: Optional[str] = "SeldonDeployment"
    metadata: Optional[SeldonMetadata] = {"name": "seldon_model"}
    specs: Optional[SeldonSpecs] = {
        "specs":{
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
                }
            },
        }
    }
    graph: Optional[SeldonGraph] = {"name": "None"}
    name: Optional[str] = "default"
    replicas: Optional[int] = 1
