from sqlalchemy import Column, String, INT, TEXT

from app.base.model import RocketBaseModel


class Config(RocketBaseModel):
    __tablename__ = "http_config"

    name = Column(String(128), nullable=False, comment="环境名")
    status = Column(INT, default=1, comment="状态 1：启用 2：禁用")
    desc = Column(String(200), comment="描述")
    config = Column(TEXT, comment="配置信息： 包含headers，variables，hooks，service，parameters")
