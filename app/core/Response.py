from pydantic import Field
from typing import TypeVar, Generic
from datetime import datetime
from pydantic.generics import GenericModel
from pydantic import BaseModel

DataT = TypeVar("DataT")


class ResponseDto(GenericModel, Generic[DataT]):
    code: int = Field(200, title="返参code")
    msg: str = Field('请求成功', title="返参msg")
    data: DataT = Field(None, title="返参data")  # 可能data没数据，没数据为null

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


class ListDto(GenericModel, Generic[DataT]):
    lists: DataT


class ListResponseDto(ResponseDto, Generic[DataT]):
    paging: dict = Field(...)
    data: DataT = None


class BaseDto(BaseModel):
    id: int
    create_time: datetime
    update_time: datetime
    deleted: int

    # 返参基础模型
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


def list_object_exclude(fields: list):
    exclude_map = {"data": {"__all__": {*fields}}}
    return exclude_map


def object_exclude(fields: list):
    exclude_map = {"data": {*fields}}
    return exclude_map


def list_exclude(fields: list):
    exclude_map = {"data": {"__all__": {*fields}}}
    return exclude_map


class Response(object):

    @staticmethod
    def model_to_dict(obj, *ignore: str):
        data = dict()
        for c in obj.__table__.columns:
            if c.name in ignore:
                # 如果字段忽略, 则不进行转换
                continue
            val = getattr(obj, c.name)
            if isinstance(val, datetime):
                data[c.name] = val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[c.name] = val
        return data

    @staticmethod
    def model_to_list(data: list, *ignore: str):
        return [Response.model_to_dict(x, *ignore) for x in data]

    @staticmethod
    def base_response(code, msg, data=None):
        return dict(code=code, msg=msg, data=data)

    @staticmethod
    def success(msg="操作成功", data=None):
        return Response.base_response(200, msg=msg, data=data)

    @staticmethod
    def failed(msg="操作失败", data=None):
        return Response.base_response(code=-1, msg=msg, data=data)
