from app.base.curd import BaseCurd
from app.models.http.plan import Plan, PlanDetail


class PlanFacade(BaseCurd):
    model = Plan

    @classmethod
    async def get_detail_with_id(cls, pk):
        return cls.get_with_id(pk=pk)


class PlanDetailFacade(BaseCurd):
    model = PlanDetail

    @classmethod
    async def list_all(cls, plan_id: int):
        return cls.get_with_params(plan_id=plan_id)
