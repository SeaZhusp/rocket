import json
from typing import List, Union

from pydantic import Field, validator

from app.base.schema import RocketBaseSchema


class Variable(RocketBaseSchema):
    key: str
    type: int
    value: Union[str, int, float, bool, list, dict]
    desc: str


class Header(RocketBaseSchema):
    key: str
    value: str
    desc: str


class FormData(RocketBaseSchema):
    key: str
    type: int
    value: Union[str, int, float, bool, list, dict]
    desc: str


class Request(RocketBaseSchema):
    data_type: str
    json_data: str
    form_data: Union[List[FormData]]


class Validator(RocketBaseSchema):
    actual: str
    comparator: str
    type: int
    expect: Union[str, int, float, bool, list, dict]
    desc: str


class Extract(RocketBaseSchema):
    key: str
    value: str
    desc: str


class SetupHook(RocketBaseSchema):
    setup_hook: str


class TeardownHook(RocketBaseSchema):
    teardown_hook: str


class Hooks(RocketBaseSchema):
    setup_hooks: List[SetupHook]
    teardown_hooks: List[TeardownHook]


class Body(RocketBaseSchema):
    variables: Union[List[Variable], None] = None
    headers: Union[List[Header], None] = None
    request: Union[Request, None] = None
    validator: Union[List[Validator], None] = None
    extract: Union[List[Extract], None] = None
    hooks: Union[Hooks, None] = None


class ApiCreateBody(RocketBaseSchema):
    name: str = Field(..., title='接口名称', description='必传')
    level: str = Field(..., title='优先级', description='必传')
    status: int = Field(..., title='状态', description='必传')
    desc: Union[str, None]
    service: str = Field(..., title='微服务', description='必传')
    method: str = Field(..., title='请求方式', description='必传')
    path: str = Field(..., title='请求路径', description='必传')
    times: int = Field(..., title='循环次数', description='必传')
    body: Body

    project_id: int = Field(..., title='项目id', description='必传')
    catalog_id: int = Field(..., title='目录id', description='必传')
    create_user: Union[str, None]
    update_user: Union[str, None]

    @validator('body')
    def body_to_str(cls, v):
        return json.dumps(v.dict())


class ApiUpdateBody(ApiCreateBody):
    id: int = Field(..., title='接口id', description='必传')
