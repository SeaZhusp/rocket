import json
from typing import Union

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema, EnvConfig


class EnvCreateBody(RocketBaseSchema):
    name: str = Field(..., title="环境名称", description="必传")
    status: int = Field(..., title="状态", description="必传")
    desc: Union[str, None]
    config: EnvConfig

    @validator('config')
    def config_to_str(cls, v):
        return json.dumps(v.dict())


class EnvUpdateBody(EnvCreateBody):
    id: int = Field(..., title='环境id', description='必传')
