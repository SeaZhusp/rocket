import json

from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Response import ListResponseDto, ResponseDto
from app.curd.http.testcase import TestcaseDao
from app.schema.http.testcase.testcase_in import TestcaseCreateBody, TestcaseUpdateBody
from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/testcase")


@router.get("/list")
async def list_testcase(project_id: int, catalog_id="", status="", level="", search="", page: int = 1,
                        limit: int = 10, user_info=Depends(Permission())):
    total, testcases = await TestcaseDao.list(project_id, catalog_id, status, level, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=testcases)


@router.post("/create")
async def create_testcase(testcase: TestcaseCreateBody, user_info=Depends(Permission())):
    fullname = user_info.get("fullname", "系统")
    await TestcaseDao.create(testcase, fullname)
    return ResponseDto(msg="创建成功")


@router.put("/update")
async def update_api(testcase: TestcaseUpdateBody, user_info=Depends(Permission())):
    fullname = user_info.get("fullname", "系统")
    await TestcaseDao.update(testcase, fullname)
    return ResponseDto(msg="更新成功")


@router.delete("/delete/{pk}")
async def delete_testcase(pk: int, user_info=Depends(Permission())):
    await TestcaseDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")
