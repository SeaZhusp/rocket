from sqlalchemy import Column, String, INT
from sqlalchemy.dialects.mysql import LONGTEXT

from app.base.model import RocketBaseModel


class Report(RocketBaseModel):
    __tablename__ = "http_report"

    name = Column(String(100), comment="报告名称")
    test_begin_time = Column(String(32), comment="测试开始时间")
    duration = Column(String(32), comment="耗时")
    create_user = Column(String(10), comment="创建人")
    total = Column(INT, comment="执行case总数")
    passed = Column(INT, comment="通过数")
    failed = Column(INT, comment="失败数")
    pass_rate = Column(String(10), comment="通过率")
    env_name = Column(String(128), comment="执行环境名")

    project_id = Column(INT, comment="项目ID")


class ReportDetail(RocketBaseModel):
    __tablename__ = "http_report_detail"

    report_id = Column(INT, comment="报告ID")
    summary = Column(LONGTEXT, comment="报告详情")
