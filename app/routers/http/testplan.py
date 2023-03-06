from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Response import ListResponseDto, ResponseDto
from app.curd.http.testplan import TestplanDao
from app.schema.http.testplan.testplan_in import TestplanCreateBody, TestplanUpdateBody
from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/testplan")


@router.get("/list")
async def list_testplan(project_id: int, status="", search="", page: int = 1, limit: int = 10,
                        user_info=Depends(Permission())):
    total, plans = await TestplanDao.list(project_id, status, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=plans)


@router.post("/create")
async def create_testplan(testplan: TestplanCreateBody, user_info=Depends(Permission())):
    await TestplanDao.create(testplan)
    return ResponseDto(msg="创建成功")


@router.put("/update")
async def update_api(testplan: TestplanUpdateBody, user_info=Depends(Permission())):
    await TestplanDao.update(testplan)
    return ResponseDto(msg="更新成功")


@router.delete("/delete/{pk}")
async def delete_testcase(pk: int, user_info=Depends(Permission())):
    await TestplanDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")
