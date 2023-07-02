from fastapi import APIRouter, Depends

from app.core.auth import Auth
from app.core.enums import DutyEnum
from app.core.response import ResponseDto, ListResponseDto
from app.curd.manage.envconfig import EnvConfigDao
from app.schema.manage.envconfig.envconfig_in import EnvConfigCreateBody, EnvConfigUpdateBody
from app.utils.utils import ComputerUtils

router = APIRouter(prefix="/scene")


@router.get("/list")
async def list_env(search="", page: int = 1, limit: int = 10, user_info=Depends(Auth())):
    total, envs = await EnvConfigDao.list(search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=envs)


@router.get("/all")
async def list_all_enable_env(user_info=Depends(Auth())):
    configs = await EnvConfigDao.list_all_enable()
    return ResponseDto(data=configs)


@router.post("/create")
async def create_env(env: EnvConfigCreateBody, user_info=Depends(Auth(DutyEnum.admin))):
    await EnvConfigDao.create(env)
    return ResponseDto(msg="创建成功")


@router.delete("/delete/{pk}")
async def delete_env(pk: int, user_info=Depends(Auth(DutyEnum.admin))):
    await EnvConfigDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.put("/update")
async def update_env(env: EnvConfigUpdateBody, user_info=Depends(Auth())):
    await EnvConfigDao.update(env)
    return ResponseDto(msg="更新成功")
