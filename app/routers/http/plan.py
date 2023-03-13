import json
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Depends

from app.core.dingtalk import DingTalk
from app.facade.http.report import ReportFacade
from app.utils.logger import log_exception
from config import Config

from app.core.auth import Auth
from app.core.enums import CatalogUsedEnum
from app.core.response import ListResponseDto, ResponseDto
from app.curd.manage.catalog import CatalogDao
from app.curd.http.plan import PlanDao, PlanDetailDao
from app.facade.http.api import ApiFacade
from app.facade.http.envconfig import EnvConfigFacade
from app.facade.http.testcase import TestcaseFacade
from app.libs.http_run import HttpRunning
from app.schema.http.plan.plan_in import PlanCreateBody, PlanUpdateBody, PlanDetailCreateBody
from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/plan")

executor = ThreadPoolExecutor(Config.EXECUTOR_THREAD_POOL)


@router.get("/list")
async def list_plan(project_id: int, status="", search="", page: int = 1, limit: int = 10,
                    user_info=Depends(Auth())):
    total, plans = await PlanDao.list(project_id, status, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=plans)


@router.post("/create")
async def create_plan(plan: PlanCreateBody, user_info=Depends(Auth())):
    await PlanDao.create(plan)
    return ResponseDto(msg="创建成功")


@router.put("/update")
async def update_plan(plan: PlanUpdateBody, user_info=Depends(Auth())):
    await PlanDao.update(plan)
    return ResponseDto(msg="更新成功")


@router.delete("/delete/{pk}")
async def delete_plan(pk: int, user_info=Depends(Auth())):
    await PlanDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.post("/run/{pk}")
async def run_plan(pk: int, user_info=Depends(Auth())):
    plan = await PlanDao.get_detail_with_id(pk=pk)
    details = await PlanDetailDao.list_all(pk)
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
    executor.submit(execute_plan, testcases, config, plan, env_name, user_info.get("fullname", "系统执行")) \
        .add_done_callback(log_exception)
    return ResponseDto(msg="后台执行中，请稍后前往报告中心查看")


@router.get("/detail/catalog/tree")
async def get_plan_detail_tree(plan_id: int, project_id: int, user_info=Depends(Auth())):
    details = await PlanDetailDao.list_all(plan_id)
    testcase_ids = [detail.testcase_id for detail in details]
    testcases = await TestcaseFacade.list_all_by_ids(testcase_ids)
    catalog_ids = [testcase.catalog_id for testcase in testcases]
    tree = await CatalogDao.get_catalog_tree_with_ids(catalog_ids, CatalogUsedEnum.TESTCASE, project_id)
    return ResponseDto(data=tree)


@router.get("/detail/testcase/list")
async def list_plan_detail_testcase(plan_id: int, catalog_id="", page: int = 1, limit: int = 10,
                                    user_info=Depends(Auth())):
    details = await PlanDetailDao.list_all(plan_id)
    testcase_ids = [detail.testcase_id for detail in details]
    total, testcases = await TestcaseFacade.list_by_ids_with_condition(testcase_ids, catalog_id)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=testcases)


@router.post("/detail/testcase/remove")
async def remove_plan_detail_testcase(plan_detail: PlanDetailCreateBody, user_info=Depends(Auth())):
    await PlanDetailDao.remove_testcase(plan_detail)
    return ResponseDto(msg="删除成功")


@router.post("/detail/testcase/add")
async def add_plan_detail_testcase(plan_detail: PlanDetailCreateBody, user_info=Depends(Auth())):
    await PlanDetailDao.create(plan_detail)
    return ResponseDto(msg="添加成功")


def execute_plan(testcases, config, plan, env_name, create_user):
    http_run = HttpRunning(testcases, config.to_dict())
    summary = http_run.run_testcase()
    report_info = {
        "name": plan.name,
        "test_begin_time": summary["stat"][0]["start_time"],
        "duration": summary["stat"][0]["duration"],
        "create_user": create_user,
        "total": summary["stat"][0]["total"],
        "passed": summary["stat"][0]["success"],
        "failed": summary["stat"][0]["failed"],
        "pass_rate": "{}%".format(round(summary["stat"][0]["success"] / summary["stat"][0]["total"], 1)),
        "env_name": env_name,
        "project_id": plan.project_id,
        "summary": json.dumps(summary)
    }
    report = ReportFacade.create(report_info)
    ding_talk = DingTalk(plan.webhook)
    ding_talk.send_msg(report_url="http://127.0.0.1:5555/#/http/report/view?report_id={}".format(report.id),
                       **report_info)