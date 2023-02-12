from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.core.Response import ResponseDto
from app.curd.system.env import EnvDao
from app.schema.system.env.env_in import EnvCreateBody

router = APIRouter(prefix='/env')


@router.post('/create')
async def create_env(env: EnvCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await EnvDao.create(env)
    return ResponseDto(msg='创建成功')
