from app.base.dto import RocketBaseDto


class UserDto(RocketBaseDto):
    username: str
    fullname: str
    email: str
    phone: str
    duty: int
    status: int
