from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.core.Response import ListResponseDto, ResponseDto
from app.curd.system.dictionary import DictDao, DictItemDao
from app.schema.system.dicts.dictionary_in import DictCreateBody, DictUpdateBody, DictItemCreateBody, DictItemUpdateBody
from app.utils.utils import Utils

router = APIRouter(prefix='/dict')


@router.get('/list')
async def list_dict(page: int = 1, limit: int = 10, search: str = None, user_info=Depends(Permission(DutyEnum.admin))):
    total, dicts = await DictDao.query_by_name(page=page, limit=limit, search=search)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=dicts)


@router.post('/create')
async def create(_dict: DictCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await DictDao.create(_dict)
    return ResponseDto(msg="创建成功")


@router.delete('/delete/{ident}')
async def delete(ident: int, user_info=Depends(Permission(DutyEnum.admin))):
    await DictDao.delete_by_id(ident=ident)
    return ResponseDto(msg="删除成功")


@router.put('/update')
async def update(_dict: DictUpdateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await DictDao.update(_dict)
    return ResponseDto(msg="更新成功")


@router.get('/item/list')
async def list_dict_item(search: int, user_info=Depends(Permission(DutyEnum.admin))):
    dict_items = await DictItemDao.query_by_name(search)
    return ResponseDto(data=dict_items)


@router.post('/item/create')
async def create_item(dict_item: DictItemCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await DictItemDao.create(dict_item)
    return ResponseDto(msg="创建成功")


@router.put('/item/update')
async def update_item(dict_item: DictItemUpdateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await DictItemDao.update(dict_item)
    return ResponseDto(msg="更新成功")


@router.delete('/item/delete/{ident}')
async def delete_item(ident: int, user_info=Depends(Permission(DutyEnum.admin))):
    await DictItemDao.delete_by_id(ident=ident)
    return ResponseDto(msg="删除成功")
