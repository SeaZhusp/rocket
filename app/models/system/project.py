from sqlalchemy import Column, String, INT

from app.base.model import RocketBaseModel


class Project(RocketBaseModel):
    __tablename__ = 'sys_project'

    name = Column(String(16), unique=True, index=True, nullable=False, comment="项目名")
    type = Column(INT, nullable=False, comment="0:api 1:web 2:app")
    owner = Column(INT, nullable=False, comment='项目所有者')
    description = Column(String(200), comment="描述")
