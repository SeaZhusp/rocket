import json

from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.curd.system.project import ProjectDao
from app.utils.utils import Utils
from app.schema.system.project.project_in import ProjectCreateBody, ProjectUpdateBody
from app.core.Response import ListResponseDto, ResponseDto

router = APIRouter(prefix="/project")


@router.post("/create")
async def create(project: ProjectCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await ProjectDao.create(project)
    return ResponseDto(msg='创建成功')


@router.get('/list')
async def list_project(page: int = 1, limit: int = 10, search: str = None, user_info=Depends(Permission())):
    total, projects = await ProjectDao.query_with_name(page=page, limit=limit, search=search)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=projects)


@router.delete('/delete/{id}')
async def delete_user(id: int, user_info=Depends(Permission(DutyEnum.admin))):
    # await ProjectDao.delete_by_id(user_id=id)
    return ResponseDto(msg="删除成功")
