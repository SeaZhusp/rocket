from typing import Union, List
from pydantic import BaseModel

ERROR_MSG_TEMPLATES = {
    "value_error.missing": "必须传值",
    "value_error.extra": "不允许额外字段",
    "type_error.none.not_allowed": "不能为空",
    "type_error.bool": "必须为bool类型",
    "value_error.byte": "必须为byte类型",
    "value_error.dict": "必须为object类型",
    "value_error.email": "不是有效的邮箱地址",
    "type_error.integer": "必须为int类型",
    "type_error.float": "必须为float类型",
    "type_error.path": "不是有效的路径",
    "type_error.list": "必须为list类型",
    "type_error.str": "必须为str类型",
    "type_error.enum": "类型有误"
}


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
