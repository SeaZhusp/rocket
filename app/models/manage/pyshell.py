from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGTEXT

from app.base.model import RocketBaseModel


class Pyshell(RocketBaseModel):
    __tablename__ = "manage_pyshell"

    module_name = Column(String(32), nullable=False, comment="名称")
    code = Column(LONGTEXT, comment="代码")
