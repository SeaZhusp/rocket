from sqlalchemy import Column, INT, String, DATETIME

from app.base.model import RocketBaseModel
from app.core.Enums import DataPermissionEnum, StatusEnum


class User(RocketBaseModel):
    __tablename__ = "sys_user"

    username = Column(String(16), unique=True, index=True, comment="账号")
    fullname = Column(String(16), index=True, comment="姓名")
    password = Column(String(32), unique=False, comment="密码")
    email = Column(String(64), unique=True, comment="邮箱")
    phone = Column(String(16), unique=True, comment="手机号")
    data_permission = Column(INT, default=DataPermissionEnum.member.value, comment="0: 普通用户 1: 组长 2: 超级管理员")
    status = Column(INT, default=StatusEnum.enable.value, comment="0:启用 1:禁用")

    def __init__(self, form):
        self.username = form.username
        self.password = form.password
        self.email = form.email
        self.phone = form.phone
        self.fullname = form.fullname
