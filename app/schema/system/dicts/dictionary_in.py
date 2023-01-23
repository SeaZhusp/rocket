from typing import Union

from pydantic import Field

from app.base.schema import RocketBaseSchema


class DictCreateBody(RocketBaseSchema):
    name: str = Field(..., title="字典名称", description="必传")
    code: str = Field(..., title="字典编号", description="必传")
    type: int = Field(..., title="字典类型", description="必传")
    description: Union[str, None]


class DictUpdateBody(DictCreateBody):
    id: int
    status: int


class DictItemCreateBody(RocketBaseSchema):
    dict_id: int = Field(..., title="字典id", description="必传")
    label: str = Field(..., title="字典项Label", description="必传")
    value: str = Field(..., title="字典项value", description="必传")
    sort: int = Field(1, title="字典项排序", description="必传")


class DictItemUpdateBody(DictItemCreateBody):
    id: int
    status: int
