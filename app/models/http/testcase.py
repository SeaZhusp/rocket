from sqlalchemy import Column, String, INT, SMALLINT, TEXT

from app.base.model import RocketBaseModel


class TestCase(RocketBaseModel):
    __tablename__ = "http_testcase"

    name = Column(String(128), nullable=False, comment="用例名称")
    desc = Column(String(200), comment="备注")
    level = Column(String(2), nullable=False, comment="优先级")
    tag = Column(String(128), comment="标签")
    status = Column(INT, default=1, comment="状态 1:启用 2:禁用")
    steps = Column(TEXT, comment="用例步骤")
