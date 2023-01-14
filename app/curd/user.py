from datetime import datetime

from sqlalchemy import or_

from app.core.Exceptions import NormalException
from app.models import Session
from app.models.user import User
from app.schema.user import UserRegisterForm, UserLoginForm
from app.libs.logger import Log


class UserDao(object):
    log = Log("UserDao")

    @staticmethod
    async def register_user(user: UserRegisterForm):
        with Session() as session:
            users = session.query(User).filter(or_(User.username == user.username, User.email == user.email)).all()
            if users:
                raise NormalException(detail="用户名或邮箱已存在")
            user = User(user)
            session.add(user)
            session.commit()

    @staticmethod
    async def login(form: UserLoginForm):
        with Session() as session:
            # 查询用户名/密码匹配且没有被删除的用户
            user = session.query(User).filter(User.username == form.username, User.password == form.password,
                                              User.deleted == 0).first()
            if user is None:
                raise Exception("用户名或密码错误")
            # 更新用户的最后登录时间
            user.last_login_time = datetime.now()
            session.commit()
            return user

    @staticmethod
    async def get_user_by_id(user_id: int):
        with Session() as session:
            user = session.query(User).get(user_id)
            return user
