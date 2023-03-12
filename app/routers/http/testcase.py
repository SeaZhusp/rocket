import json

from fastapi import APIRouter, Depends

from app.core.auth import Auth
from app.core.response import ListResponseDto, ResponseDto
from app.curd.http.testcase import TestcaseDao
from app.facade.http.api import ApiFacade
from app.facade.http.envconfig import EnvConfigFacade
from app.schema.http.testcase.testcase_in import TestcaseCreateBody, TestcaseUpdateBody, TestcaseRunBody
from app.utils.utils import ComputerUtils
from app.core.httpexecutor import HttpRunning

router = APIRouter(prefix="/testcase")


@router.get("/list")
async def list_testcase(project_id: int, catalog_id="", status="", level="", search="", page: int = 1,
                        limit: int = 10, user_info=Depends(Auth())):
    total, testcases = await TestcaseDao.list(project_id, catalog_id, status, level, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=testcases)


@router.post("/create")
async def create_testcase(testcase: TestcaseCreateBody, user_info=Depends(Auth())):
    fullname = user_info.get("fullname", "系统")
    await TestcaseDao.create(testcase, fullname)
    return ResponseDto(msg="创建成功")


@router.put("/update")
async def update_api(testcase: TestcaseUpdateBody, user_info=Depends(Auth())):
    fullname = user_info.get("fullname", "系统")
    await TestcaseDao.update(testcase, fullname)
    return ResponseDto(msg="更新成功")


@router.delete("/delete/{pk}")
async def delete_testcase(pk: int, user_info=Depends(Auth())):
    await TestcaseDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.post("/run")
async def run_testcase(case: TestcaseRunBody, user_info=Depends(Auth())):
    case = await TestcaseDao.get_detail_with_id(pk=case.id)
    steps = json.loads(case.body).get("steps")
    apis = []
    for step in steps:
        if step.get("status") != 1:
            continue
        api = await ApiFacade.get_detail_with_id(step.get("id"))
        apis.append(api.to_dict())
    config = await EnvConfigFacade.get_detail_with_id(pk=case.env_id)
    http_run = HttpRunning([{"case_id": case.id, "testcase": apis}], config.to_dict())
    summary = http_run.run_testcase()
    return ResponseDto(data=summary)
