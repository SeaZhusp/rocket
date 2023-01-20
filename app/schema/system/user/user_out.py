from app.core.Response import BaseDto


class UserDto(BaseDto):
    username: str
    fullname: str
    email: str
    phone: str
    duty: int
    status: int
