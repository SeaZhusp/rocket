import json
from typing import Union

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema


class TestplanCreateBody(RocketBaseSchema):
    name: str = Field(..., title="接口名称", description="必传")
    status: int = Field(..., title="状态", description="必传")
    desc: Union[str, None]

    env_id: Union[int, None]
    project_id: int = Field(..., title="项目id", description="必传")
    catalog_id: int = Field(..., title="目录id", description="必传")
    create_user: Union[str, None]


class TestplanUpdateBody(TestplanCreateBody):
    id: int = Field(..., title="接口id", description="必传")


class TestplanRunBody(RocketBaseSchema):
    id: int
