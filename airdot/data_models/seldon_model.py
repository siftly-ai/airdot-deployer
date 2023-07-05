from pydantic import BaseModel
from typing_extensions import Literal
from typing import Optional

class SeldonMetadata(BaseModel):
    pass

class SeldonSpecs(BaseModel):
    pass

class SeldonGraph(BaseModel):
    pass

class SeldonConfiguration(BaseModel):
    apiVersion: Optional[Literal['machinelearning.seldon.io/v1', 'machinelearning.seldon.io/v1alpha2']] = 'machinelearning.seldon.io/v1'
    kind: Optional[str] = 'SeldonDeployment'
    metadata: Optional[SeldonMetadata] = {'name': 'None'}
    specs: Optional[SeldonSpecs] = {
        'name': 'None',
        'predictors': {
            'componentSpecs':{
                'specs': {
                    'container':{
                        'name':'None',
                        'image':'None',
                        'imagePullPolicy' :'ifNotPresent',
                        'resources': {
                            'requests':{
                                'cpu':'1',
                                'memory':'1M'
                            }
                        }
                    }
                }
            }
        }
    }
    graph:Optional[SeldonGraph] = {'name':'None'}
    name: Optional[str] = 'default'
    replicas: Optional[int] = 1