from sqlalchemy import Column, String, INT, SMALLINT, TEXT

from app.base.model import RocketBaseModel


class Testcase(RocketBaseModel):
    __tablename__ = "http_testcase"

    name = Column(String(128), nullable=False, comment="用例名称")
    desc = Column(String(200), comment="备注")
    level = Column(String(2), nullable=False, comment="优先级")
    tags = Column(String(128), comment="标签")
    status = Column(INT, default=1, comment="状态 1:启用 2:禁用")
    body = Column(TEXT, comment="用例步骤")

    catalog_id = Column(INT, nullable=False, comment="目录id")
    project_id = Column(INT, nullable=False, comment="项目id")
    create_user = Column(String(16), nullable=False, comment="创建人")
    update_user = Column(String(16), nullable=False, comment="修改人")
    env_id = Column(INT, comment="环境id")
