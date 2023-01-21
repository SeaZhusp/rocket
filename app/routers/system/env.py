from fastapi import APIRouter

from app.core.Response import ResponseDto
from app.curd.system.env import EnvDao
from app.schema.system.env.env_in import EnvCreateBody

router = APIRouter(prefix='/env')


@router.post('/create')
async def create(env: EnvCreateBody):
    await EnvDao.create(env)
    return ResponseDto(msg='创建成功')
