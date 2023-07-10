from fastapi import APIRouter, Depends

from app.core.auth import Auth
from app.core.enums import DutyEnum
from app.curd.manage.project import ProjectDao
from app.utils.utils import ComputerUtils
from app.schema.manage.project.project_in import ProjectCreateBody, ProjectUpdateBody
from app.core.response import ListResponseDto, ResponseDto

router = APIRouter(prefix="/project")


@router.post("/create")
async def create_project(project: ProjectCreateBody, user_info=Depends(Auth(DutyEnum.admin))):
    await ProjectDao.create(project)
    return ResponseDto(msg="创建成功")


@router.get("/list")
async def list_project(page: int = 1, limit: int = 10, search: str = None,
                       user_info=Depends(Auth(DutyEnum.admin))):
    total, projects = await ProjectDao.list(page=page, limit=limit, search=search)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=projects)


@router.delete("/delete/{pk}")
async def delete_project(pk: int, user_info=Depends(Auth(DutyEnum.admin))):
    await ProjectDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.put("/update")
async def update_project(project: ProjectUpdateBody, user_info=Depends(Auth(DutyEnum.admin))):
    await ProjectDao.update(project)
    return ResponseDto(msg="更新成功")


@router.get("/all")
async def list_all_project(user_info=Depends(Auth())):
    projects = await ProjectDao.list_all()
    return ResponseDto(data=projects)
