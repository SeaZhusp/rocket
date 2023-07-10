import json
from typing import Union, List

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema, TestcaseBody


class TestcaseCreateBody(RocketBaseSchema):
    name: str = Field(..., title="接口名称", description="必传")
    level: str = Field(..., title="优先级", description="必传")
    status: int = Field(..., title="状态", description="必传")
    tags: Union[List[str], None]
    desc: Union[str, None]
    body: TestcaseBody

    env_id: Union[int, None]
    project_id: int = Field(..., title="项目id", description="必传")
    catalog_id: int = Field(..., title="目录id", description="必传")
    create_user: Union[str, None]
    update_user: Union[str, None]

    @validator("body")
    def body_to_str(cls, v):
        return json.dumps(v.dict(), ensure_ascii=False)

    @validator("tags")
    def tags_to_str(cls, v):
        return json.dumps(v, ensure_ascii=False)


class TestcaseUpdateBody(TestcaseCreateBody):
    id: int = Field(..., title="接口id", description="必传")


class TestcaseRunBody(RocketBaseSchema):
    id: int
