import json
from typing import Union, List

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema, EnvConfig


class EnvConfigCreateBody(RocketBaseSchema):
    name: str = Field(..., title="环境名称", description="必传")
    status: int = Field(..., title="状态", description="必传")
    modules: Union[List[str], None]
    desc: Union[str, None]
    config: EnvConfig

    @validator("config")
    def config_to_str(cls, v):
        return json.dumps(v.dict())

    @validator("modules")
    def modules_to_str(cls, v):
        return json.dumps(v)


class EnvConfigUpdateBody(EnvConfigCreateBody):
    id: int = Field(..., title="环境id", description="必传")
