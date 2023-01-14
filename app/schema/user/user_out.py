from datetime import datetime

from app.core.Response import BaseDto


class UserDto(BaseDto):
    username: str
    fullname: str
    email: str
    phone: str
    data_permission: int
    status: int
