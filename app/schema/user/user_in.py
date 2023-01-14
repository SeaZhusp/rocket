from typing import Union

from pydantic import BaseModel, validator, Field

from app.utils.encrypt import Encrypt
from app.core.Request import ToolsSchemas
from config import Config


class BaseUserBody(BaseModel):
    password: str
    username: str


class UserCreateBody(BaseUserBody):
    fullname: str = Field(..., max_length=16)
    email: Union[str, None] = Field(default=None, max_length=64)
    phone: Union[str, None] = Field(default=None, max_length=16)

    @validator('username', 'password', 'fullname')
    def check_fields(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('password')
    def password_to_md5(cls, v):
        return Encrypt.md5(f"{v}{Config.TOKEN_KEY}")


class UserLoginBody(BaseUserBody):

    @validator('username', 'password')
    def name_not_empty(cls, v):
        return ToolsSchemas.not_empty(v)

    @validator('password')
    def password_to_md5(cls, v):
        return Encrypt.md5(f"{v}{Config.TOKEN_KEY}")
