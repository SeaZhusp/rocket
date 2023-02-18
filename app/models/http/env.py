from sqlalchemy import Column, String, INT, TEXT

from app.base.model import RocketBaseModel


class Env(RocketBaseModel):
    __tablename__ = 'http_env'

    name = Column(String(128), nullable=False, comment='环境名')
    description = Column(String(200), comment='描述')
    config = Column(TEXT, comment='配置信息： 包含headers，variables，hooks，service，parameters')
