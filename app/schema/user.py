from pydantic import BaseModel, validator

from app.libs.utils import StringUtil
from config import Config


class UserRegisterForm(BaseModel):
    username: str
    nickname: str
    password: str
    email: str

    @validator('username', 'password', 'nickname', 'email')
    def check_fields(cls, v):
        return StringUtil.not_empty(v)

    @validator('password')
    def password_to_md5(cls, v):
        return StringUtil.to_md5(f"{v}{Config.TOKEN_KEY}")


class UserLoginForm(BaseModel):
    password: str
    username: str

    @validator('username', 'password')
    def name_not_empty(cls, v):
        return StringUtil.not_empty(v)

    @validator('password')
    def password_to_md5(cls, v):
        return StringUtil.to_md5(f"{v}{Config.TOKEN_KEY}")
