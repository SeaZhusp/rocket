from sqlalchemy import or_

from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCrud
from app.models.system.user import User
from app.schema.system.user.user_in import UserCreateBody, UserLoginBody
from app.schema.system.user.user_out import UserDto


class UserDao(BaseCrud):
    model = User

    @classmethod
    async def create(cls, body: UserCreateBody):
        filter_list = [or_(cls.model.username == body.username,
                           cls.model.email == body.email if body.email else None,
                           cls.model.phone == body.phone if body.phone else None)]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("用户名/邮箱/手机已存在")
        user = User(**body.dict())
        return cls.insert_with_model(model_obj=user)

    @classmethod
    async def login(cls, body: UserLoginBody):
        user = cls.get_with_first(username=body.username, password=body.password)
        if user is None:
            raise BusinessException("用户名或密码错误")
        if user.status == 0:
            raise BusinessException("账号已被禁用,请联系管理员")
        return user

    @classmethod
    async def query_with_fullname(cls, page: int = 1, limit: int = 10, search: str = None) -> (int, User):
        total, users = cls.get_with_pagination(page=page, limit=limit, _fields=UserDto, _sort=['create_time'],
                                               fullname=f"%{search}%" if search else None)
        return total, users

    @classmethod
    async def get_by_id(cls, user_id: int):
        user = cls.get_with_id(id=user_id)
        return user

    @classmethod
    async def delete_by_id(cls, user_id: int):
        user = cls.delete_with_id(pk=user_id)
        return user

    @classmethod
    async def update_user(cls, user: UserUpdateBody):
        user = cls.update_with_id(model=user)
        return user
