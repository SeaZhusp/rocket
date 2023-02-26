from sqlalchemy import Column, String, UniqueConstraint

from app.base.model import RocketBaseModel


class Project(RocketBaseModel):
    __tablename__ = "manage_project"

    name = Column(String(16), index=True, nullable=False, comment="项目名")
    description = Column(String(200), comment="描述")
