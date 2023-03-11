from app.base.curd import BaseCurd
from app.models.http.envconfig import EnvConfig
from app.models.http.plan import Plan, PlanDetail


class PlanDao(BaseCurd):
    model = Plan

    @classmethod
    async def list(cls, project_id: int, status="", search="", page: int = 1, limit: int = 10):
        kwargs = {}
        if status != "":
            kwargs.update(status=status)
        if project_id != "":
            kwargs.update(project_id=project_id)
        if search != "":
            kwargs.update(name=f"%{search}%")
        # total, apis = cls.get_with_pagination(page=page, limit=limit, _sort=["create_time"], **kwargs)
        total, plans = cls.get_with_join(page=page, limit=limit, query_fields=[EnvConfig.name],
                                         join_con=[EnvConfig, EnvConfig.id == Plan.env_id])
        return total, plans

    @classmethod
    async def create(cls, plan):
        o = Plan(**plan.dict())
        cls.insert_with_model(model_obj=o)

    @classmethod
    async def update(cls, plan):
        return cls.update_with_id(model=plan)

    @classmethod
    async def delete(cls, pk: int):
        cls.delete_with_id(pk=pk)

    @classmethod
    async def get_detail_with_id(cls, pk):
        return cls.get_with_id(pk=pk)


class PlanDetailDao(BaseCurd):
    model = PlanDetail

    @classmethod
    async def list_all(cls, plan_id: int):
        return cls.get_with_params(plan_id=plan_id)

    @classmethod
    async def list_testcase(cls, plan_id: int, page: int = 1, limit: int = 10):
        # todo
        details = cls.get_with_pagination(page=page, limit=limit)
        testcase_ids = [detail.testcase_id for detail in details]

    @classmethod
    async def remove_testcase(cls, plan_detail):
        cls.delete_with_params(plan_id=plan_detail.plan_id, testcase_id=plan_detail.testcase_id)

    @classmethod
    async def create(cls, plan_detail):
        o = PlanDetail(**plan_detail.dict())
        cls.insert_with_model(model_obj=o)
