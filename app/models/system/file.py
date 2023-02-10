from sqlalchemy import Column, String, INT

from app.base.model import RocketBaseModel


class File(RocketBaseModel):
    __tablename__ = 'http_file'

    name = Column(String(16), nullable=False, comment='文件名')
    size = Column(INT, comment='文件大小')
    file_type = Column(String(8), comment='文件类型')
    path = Column(String(200), comment='文件路径')
