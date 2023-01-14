from datetime import datetime
from sqlalchemy import Column, INT, DATETIME

from app.models import Base


class RocketBaseModel(Base):
    id = Column(INT, primary_key=True)
    create_time = Column(DATETIME, default=datetime.now, nullable=False)
    update_time = Column(DATETIME, default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted = Column(INT, default=0, comment="0:未删除 1:已删除")
    # 设置为True，代表为基类，不会被创建为表
    __abstract__ = True
