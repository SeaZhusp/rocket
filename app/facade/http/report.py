from app.base.curd import BaseCurd
from app.models.http.report import Report


class ReportFacade(BaseCurd):
    model = Report

    @classmethod
    def create(cls, report):
        o = Report(**report)
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def info(cls, pk):
        return cls.get_with_id(pk=pk)
