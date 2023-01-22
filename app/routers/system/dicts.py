from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.core.Response import ListResponseDto, ResponseDto
from app.curd.system.dicts import DictDao
from app.schema.system.dicts.dict_in import DictCreateBody
from app.utils.utils import Utils

router = APIRouter(prefix='/dict')


@router.get('/list')
async def list_dict(page: int = 1, limit: int = 10, search: str = None, user_info=Depends(Permission(DutyEnum.admin))):
    total, dicts = await DictDao.query_with_name(page=page, limit=limit, search=search)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=dicts)


@router.post('/create')
async def create(_dict: DictCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await DictDao.create(_dict)
    return ResponseDto(msg="创建成功")
