import json

from app.curd.http.plan import PlanDao, PlanDetailDao
from app.curd.facade.http.api import ApiFacade
from app.curd.facade.http.envconfig import EnvConfigFacade
from app.curd.facade.http.testcase import TestcaseFacade


class HttpMixFacade(object):

    @classmethod
    async def get_execute_plan_kwargs(cls, plan_id, create_user):
        plan = await PlanDao.get_detail_with_id(pk=plan_id)
        details = await PlanDetailDao.list_all(plan_id)
        testcase_ids = [detail.testcase_id for detail in details]
        cases = await TestcaseFacade.list_all_by_ids(testcase_ids)
        testcases = []
        for case in cases:
            apis = []
            steps = json.loads(case.body).get("steps")
            if not steps:
                continue
            for step in steps:
                if step.get("status") != 1:
                    continue
                api = await ApiFacade.get_detail_with_id(step.get("id"))
                apis.append(api.to_dict())
            testcases.append({"case_id": case.id, "testcase": apis})
        config = await EnvConfigFacade.get_detail_with_id(pk=plan.env_id)
        env_name = config.name
        return {
            "plan_id": plan_id,
            "testcases": testcases,
            "config": config,
            "plan": plan,
            "env_name": env_name,
            "create_user": create_user,
            "cron": plan.cron,
            "plan_name": plan.name
        }
