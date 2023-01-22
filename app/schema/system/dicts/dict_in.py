from typing import Union

from pydantic import Field

from app.base.schema import RocketBaseSchema


class DictCreateBody(RocketBaseSchema):
    name: str = Field(..., title="字典名称", description="必传")
    code: str = Field(..., title="字典编号", description="必传")
    type: int = Field(..., title="字典类型", description="必传")
    description: Union[str, None]
