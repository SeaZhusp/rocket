import json
from typing import Union

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema, Body


class ApiCreateBody(RocketBaseSchema):
    name: str = Field(..., title="接口名称", description="必传")
    level: str = Field(..., title="优先级", description="必传")
    status: int = Field(..., title="状态", description="必传")
    desc: Union[str, None]
    service: str = Field(..., title="微服务", description="必传")
    method: str = Field(..., title="请求方式", description="必传")
    path: str = Field(..., title="请求路径", description="必传")
    times: int = Field(..., title="循环次数", description="必传")
    body: Body

    project_id: int = Field(..., title="项目id", description="必传")
    catalog_id: int = Field(..., title="目录id", description="必传")
    config_id: int
    create_user: Union[str, None]
    update_user: Union[str, None]

    @validator("body")
    def body_to_str(cls, v):
        return json.dumps(v.dict())


class ApiUpdateBody(ApiCreateBody):
    id: int = Field(..., title="接口id", description="必传")


class SingleApiRunBody(RocketBaseSchema):
    api_id: int
    config_id: int
