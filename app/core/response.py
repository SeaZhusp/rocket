from pydantic import Field
from typing import TypeVar, Generic
from datetime import datetime
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class ResponseDto(GenericModel, Generic[DataT]):
    code: int = Field(200, title="返参code")
    msg: str = Field("请求成功", title="返参msg")
    data: DataT = Field(None, title="返参data")  # 可能data没数据，没数据为null

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


class ListResponseDto(ResponseDto, Generic[DataT]):
    paging: dict = Field(...)
