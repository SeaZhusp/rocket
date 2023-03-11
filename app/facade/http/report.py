from app.base.curd import BaseCurd
from app.models.http.report import Report, ReportDetail


class ReportFacade(BaseCurd):
    model = Report

    @classmethod
    def create(cls, report):
        o = Report(**report)
        return cls.insert_with_model(model_obj=o)


class ReportDetailFacade(BaseCurd):
    model = ReportDetail

    @classmethod
    def create(cls, report_detail):
        o = ReportDetail(**report_detail)
        cls.insert_with_model(model_obj=o)
