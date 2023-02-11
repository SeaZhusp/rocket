from fastapi import APIRouter, Depends

from app.core.Response import ResponseDto, ListResponseDto
from app.core.Auth import Permission
from app.curd.http.api import ApiDao
from app.schema.http.api.api_in import ApiCreateBody
from app.utils.utils import Utils

router = APIRouter(prefix='/api')


@router.post('/create')
async def create_api(api: ApiCreateBody, user_info=Depends(Permission())):
    fullname = user_info.get('fullname', '系统')
    await ApiDao.create(api, fullname)
    return ResponseDto(msg="创建成功")


@router.get('/list')
async def list_api(project_id: int, catalog_id="", status="", level="", search="", page: int = 1,
                   limit: int = 10, user_info=Depends(Permission())):
    total, apis = await ApiDao.list(project_id, catalog_id, status, level, search, page, limit)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=apis)
