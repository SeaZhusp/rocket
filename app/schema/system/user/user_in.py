from typing import Union

from pydantic import validator, Field

from app.base.schema import RocketBaseSchema
from app.core.Enums import DutyEnum, StatusEnum
from app.utils.crypto import Crypto

from app.utils.utils import StringUtils
from config import Config


class BaseUserBody(RocketBaseSchema):
    password: str
    username: str


class UserCreateBody(BaseUserBody):
    fullname: str = Field(..., max_length=16)
    email: Union[str, None] = Field(default=None, max_length=64)
    phone: Union[str, None] = Field(default=None, max_length=16)

    @validator('username', 'password', 'fullname')
    def check_fields(cls, v):
        return StringUtils.not_empty(v)

    @validator('password')
    def password_to_md5(cls, v):
        return Crypto.md5(f"{v}{Config.TOKEN_KEY}")


class UserLoginBody(BaseUserBody):

    @validator('username', 'password')
    def name_not_empty(cls, v):
        return StringUtils.not_empty(v)

    @validator('password')
    def password_to_md5(cls, v):
        return Crypto.md5(f"{v}{Config.TOKEN_KEY}")


class UserUpdateBody(RocketBaseSchema):
    id: int = Field(..., title="用户id", description="必传")
    fullname: str = Field(None, title="姓名", description="非必传")
    phone: str = Field(None, title="手机号", description="非必传")
    email: str = Field(None, title="邮箱", description="非必传")
    duty: DutyEnum = Field(0, title="数据权限", description="非必传")
    status: StatusEnum = Field(1, title="是否冻结", description="非必传")
