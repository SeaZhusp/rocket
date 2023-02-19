from sqlalchemy import Column, String, INT

from app.base.model import RocketBaseModel


class Dict(RocketBaseModel):
    __tablename__ = "sys_dict"

    name = Column(String(16), nullable=False, comment="字典名称")
    code = Column(String(16), nullable=False, comment="字典编码")
    type = Column(INT, nullable=False, comment="0:string 1:number")
    status = Column(INT, default=1, comment="1启用 0禁用")
    description = Column(String(200), comment="描述")

    def __init__(self, form):
        self.name = form.name
        self.code = form.code
        self.type = form.type
        self.description = form.description


class DictItem(RocketBaseModel):
    __tablename__ = "sys_dict_item"

    dict_id = Column(INT, nullable=False, comment="字典id")
    label = Column(String(128), nullable=False, comment="字典项名称")
    value = Column(String(128), nullable=False, comment="字典值")
    sort = Column(INT, comment="排序")
    status = Column(INT, default=1, comment="1启用 0禁用")

    def __init__(self, form):
        self.dict_id = form.dict_id
        self.label = form.label
        self.value = form.value
        self.sort = form.sort
