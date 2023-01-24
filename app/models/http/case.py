from sqlalchemy import Column, String, INT

from app.base.model import RocketBaseModel


class Case(RocketBaseModel):
    name = Column(String(128), nullable=False, comment='用例名称')
    level = Column(String(2), nullable=False, comment='优先级：P0，P1，P2')
    status = Column(INT, default=0, comment='用例状态 0:进行中 1：已完成 2：已停用')
    tag = Column(String(128), comment='标签')
    description = Column(String(200), comment='描述')
    service = Column(String(16), nullable=False, comment='微服务')
    method = Column(String(12), nullable=False, comment='请求方式')
    path = Column(String(512), nullable=False, comment='接口请求路径')

    catalog_id = Column(INT, nullable=False, comment='目录id')
    project_id = Column(INT, nullable=False, comment='项目id')
    create_user = Column(String(16), nullable=False, comment='创建人')
    update_user = Column(String(16), nullable=False, comment='修改人')
