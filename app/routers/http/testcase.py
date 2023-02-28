from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Response import ListResponseDto
from app.curd.http.testcase import TestcaseDao
from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/testcase")


@router.get("/list")
async def list_testcase(project_id: int, catalog_id="", status="", level="", search="", page: int = 1,
                        limit: int = 10, user_info=Depends(Permission())):
    total, testcases = await TestcaseDao.list(project_id, catalog_id, status, level, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=testcases)
