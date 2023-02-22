from sqlalchemy import Column, String, INT, UniqueConstraint

from app.base.model import RocketBaseModel


class Catalog(RocketBaseModel):
    __tablename__ = "http_catalog"

    name = Column(String(32), nullable=False, comment="目录名称")
    parent_id = Column(INT, comment="父级id")
    project_id = Column(INT, nullable=False, comment="项目id")

    # 联合索引，防止同一层次出现同名目录
    __table_args__ = (
        UniqueConstraint("project_id", "name", "parent_id"),
    )
