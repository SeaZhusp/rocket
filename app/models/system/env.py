from sqlalchemy import Column, String, INT, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.base.model import RocketBaseModel


class Env(RocketBaseModel):
    __tablename__ = 'sys_env'

    name = Column(String(16), nullable=False, comment='环境名')
    description = Column(String(200), comment='描述')
    type = Column(INT, nullable=False, comment='0:api 1:web 2:app')

    def __init__(self, form):
        self.name = form.name
        self.description = form.description
        self.type = form.type


class Domain(RocketBaseModel):
    __tablename__ = 'sys_env_domain'

    domain = Column(String(256), nullable=False, comment='域名')
    description = Column(String(200), comment='描述')
    env_id = Column(INT, ForeignKey('sys_env.id'))
    env = relationship(Env, backref=backref('sys_env_domain', uselist=True))

    def __init__(self, form):
        self.domain = form.domain
        self.description = form.description
        self.env_id = form.env_id
