from sqlalchemy import Column, String, INT, TEXT

from app.base.model import RocketBaseModel


class Scene(RocketBaseModel):
    __tablename__ = "df_scene"

    name = Column(String(128), nullable=False, comment="场景名称")
    fun_name = Column(INT, nullable=False, comment="方法名")
    desc = Column(String(200), nullable=False, comment="描述")
    business = Column(String(128), nullable=False, comment="所属业务")
    header = Column(TEXT, nullable=True, comment="请求头")
    owner = Column(String(32), nullable=False, comment="负责人")
    path = Column(String(255), nullable=False, comment="脚本路径")
    param_in = Column(TEXT, nullable=True, comment="请求参数")
    param_out = Column(TEXT, nullable=True, comment="返回参数")
    example_param_in = Column(TEXT, nullable=True, comment="请求示例")
    example_param_out = Column(TEXT, nullable=True, comment="返回示例")

    project_id = Column(INT, comment="项目ID")

