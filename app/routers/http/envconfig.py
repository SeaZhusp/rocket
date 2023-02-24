from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.core.Response import ResponseDto, ListResponseDto
from app.curd.http.envconfig import EnvConfigDao
from app.schema.http.config.envconfig_in import EnvConfigCreateBody, EnvConfigUpdateBody
from app.utils.utils import Utils

router = APIRouter(prefix="/envconfig")


@router.get("/list")
async def list_env(search="", page: int = 1, limit: int = 10, user_info=Depends(Permission())):
    total, envs = await EnvConfigDao.list(search, page, limit)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=envs)


@router.get("/all")
async def list_all_enable_env(user_info=Depends(Permission())):
    configs = await EnvConfigDao.list_all_enable()
    return ResponseDto(data=configs)


@router.post("/create")
async def create_env(env: EnvConfigCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await EnvConfigDao.create(env)
    return ResponseDto(msg="创建成功")


@router.delete("/delete/{pk}")
async def delete_env(pk: int, user_info=Depends(Permission(DutyEnum.admin))):
    await EnvConfigDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.put("/update")
async def update_env(env: EnvConfigUpdateBody, user_info=Depends(Permission())):
    await EnvConfigDao.update(env)
    return ResponseDto(msg="更新成功")
