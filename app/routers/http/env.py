from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.core.Response import ResponseDto, ListResponseDto
from app.curd.http.env import EnvDao
from app.schema.http.env.env_in import EnvCreateBody, EnvUpdateBody
from app.utils.utils import Utils

router = APIRouter(prefix='/env')


@router.get('/list')
async def list_env(search="", page: int = 1, limit: int = 10, user_info=Depends(Permission())):
    total, envs = await EnvDao.list(search, page, limit)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=envs)


@router.post('/create')
async def create_env(env: EnvCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await EnvDao.create(env)
    return ResponseDto(msg='创建成功')


@router.get('/delete/{pk}')
async def delete_env(pk: int, user_info=Depends(Permission(DutyEnum.admin))):
    return ResponseDto(msg='删除成功')


@router.put('/update')
async def update_env(env: EnvUpdateBody, user_info=Depends(Permission())):
    pass
    return ResponseDto(msg='更新成功')
