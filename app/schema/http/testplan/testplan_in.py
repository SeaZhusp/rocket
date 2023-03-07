from typing import Union

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema
from app.utils.utils import StringUtils


class TestplanCreateBody(RocketBaseSchema):
    name: str = Field(..., title="接口名称", description="必传")
    cron: str = Field(..., title="cron表达式", description="必传")
    status: int = Field(..., title="状态", description="必传")
    webhook: Union[str, None]
    desc: Union[str, None]

    env_id: int = Field(..., title="环境ID", description="必传")
    project_id: int


class TestplanUpdateBody(TestplanCreateBody):
    id: int = Field(..., title="接口id", description="必传")


class TestplanRunBody(RocketBaseSchema):
    id: int
