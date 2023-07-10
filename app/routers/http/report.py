from fastapi import APIRouter, Depends

from app.core.auth import Auth
from app.core.response import ListResponseDto, ResponseDto
from app.curd.http.report import ReportDao

from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/report")


@router.get("/list")
async def list_report(project_id: int, search="", page: int = 1, limit: int = 10):
    total, envs = await ReportDao.list(project_id, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=envs)


@router.delete("/delete/{pk}")
async def delete_report(pk: int, user_info=Depends(Auth())):
    await ReportDao.delete(pk)
    return ResponseDto(msg="删除成功")


@router.get("/view")
async def get_report_info(report_id: int, user_info=Depends(Auth())):
    report_detail = await ReportDao.info(report_id)
    return ResponseDto(data=report_detail)
