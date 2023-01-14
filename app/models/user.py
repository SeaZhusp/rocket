from sqlalchemy import Column, INT, String, DATETIME

from app.base.model import RocketBaseModel
from app.core.Enums import DataPermissionEnum


class User(RocketBaseModel):
    __tablename__ = "user"

    username = Column(String(16), unique=True, index=True)
    nickname = Column(String(16), index=True)
    password = Column(String(32), unique=False)
    email = Column(String(64), unique=True, nullable=False)
    phone = Column(String(16), unique=True)
    data_permission = Column(INT, default=DataPermissionEnum.member, comment="0: 普通用户 1: 组长 2: 超级管理员")
    role_id = Column(INT)
    last_login_time = Column(DATETIME)

    def __init__(self, form):
        self.username = form.username
        self.password = form.password
        self.email = form.email
        self.nickname = form.nickname
