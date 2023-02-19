from sqlalchemy import Column, String, INT, UniqueConstraint

from app.base.model import RocketBaseModel


class Project(RocketBaseModel):
    __tablename__ = "sys_project"

    name = Column(String(16), index=True, nullable=False, comment="项目名")
    type = Column(INT, nullable=False, comment="0:api 1:web 2:app")
    description = Column(String(200), comment="描述")

    UniqueConstraint("name", "type")

    def __init__(self, form):
        self.name = form.name
        self.type = form.type
        self.description = form.description
