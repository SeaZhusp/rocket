from app.base.curd import BaseCurd
from app.models.http.report import Report


class ReportDao(BaseCurd):
    model = Report

    @classmethod
    async def list(cls, search, page, limit):
        return cls.get_with_pagination(page=page, limit=limit, _sort=["create_time"],
                                       name=f"%{search}%" if search else None)

    @classmethod
    async def delete(cls, pk):
        cls.delete_with_id(pk=pk)

    @classmethod
    async def info(cls, pk):
        return cls.get_with_id(pk=pk)
