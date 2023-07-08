from pydantic import BaseModel
from typing_extensions import Literal
from typing import Optional
from airdot.data_models.seldon_model import SeldonConfiguration
from airdot.data_models.kserve_model import KServe


class Deployment(BaseModel):
    deployment_type: Literal["seldon", "kserve", "local"]
    bucket_type: Optional[str] = None
    seldon_configuration: Optional[SeldonConfiguration]
    kserve_configuration: Optional[KServe]
