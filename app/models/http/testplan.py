from sqlalchemy import Column, String, INT

from app.base.model import RocketBaseModel


class Testplan(RocketBaseModel):
    __tablename__ = "http_testplan"

    name = Column(String(128), nullable=False, comment="用例名称")
    desc = Column(String(200), comment="备注")
    cron = Column(String(128), comment="cron表达式")
    webhook = Column(String(1024), comment="webhook 钉钉")
    status = Column(INT, default=1, comment="状态 1：创建 2：启动中 3：暂停")

    env_id = Column(INT, comment="环境ID")
    project_id = Column(INT, comment="项目ID")
