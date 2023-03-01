from typing import Union, List
from pydantic import BaseModel
from app.core.Constants import ERROR_MSG_TEMPLATES


class RocketBaseSchema(BaseModel):
    # 入参基础模型
    class Config:
        error_msg_templates = ERROR_MSG_TEMPLATES


class KeyValue(RocketBaseSchema):
    key: str
    value: str
    desc: str


class KeyTypeValue(KeyValue):
    type: int
    value: Union[str, int, float, bool, list, dict]


class Variable(KeyTypeValue):
    pass


class Header(KeyValue):
    pass


class FormData(KeyTypeValue):
    pass


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


class Extract(KeyValue):
    pass


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


class Service(KeyValue):
    pass


class EnvConfig(RocketBaseSchema):
    variables: Union[List[Variable], None] = None
    headers: Union[List[Header], None] = None
    hooks: Union[Hooks, None] = None
    service: Union[List[Service], None] = None


class Step(RocketBaseSchema):
    id: int
    name: str
    path: str
    index: int
    method: str
    status: int


class TestcaseBody(RocketBaseSchema):
    steps: Union[List[Step], None] = None
