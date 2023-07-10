from sqlalchemy import Column, String, INT, SMALLINT

from app.base.model import RocketBaseModel


class Project(RocketBaseModel):
    __tablename__ = "manage_project"

    name = Column(String(16), index=True, nullable=False, comment="项目名")
    description = Column(String(200), comment="描述")


class ProjectMember(RocketBaseModel):
    __tablename__ = "manage_project_member"

    user_id = Column(INT, nullable=False, comment="用户id")
    project_id = Column(INT, nullable=False, comment="项目id")
    project_role = Column(SMALLINT, default=0, nullable=False, comment="0: 普通用户 1: 组长")

