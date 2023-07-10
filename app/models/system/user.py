from sqlalchemy import Column, INT, String

from app.base.model import RocketBaseModel
from app.core.enums import StatusEnum, DutyEnum


class User(RocketBaseModel):
    __tablename__ = "sys_user"

    username = Column(String(16), unique=True, index=True, comment="账号")
    fullname = Column(String(16), index=True, comment="姓名")
    password = Column(String(32), unique=False, comment="密码")
    email = Column(String(64), unique=True, comment="邮箱")
    phone = Column(String(16), unique=True, comment="手机号")
    duty = Column(INT, default=DutyEnum.member.value, comment="0: 普通用户 1: 组长 2: 管理员")
    status = Column(INT, default=StatusEnum.enable.value, comment="0:启用 1:禁用")

    def __init__(self, username, fullname, password, email="", phone=""):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.fullname = fullname
