import json

from fastapi import APIRouter, Depends

from app.core.result import aaa
from app.curd.http.config import ConfigDao
from app.utils.utils import Utils
from app.curd.http.api import ApiDao
from app.core.Auth import Permission
from app.curd.system.catalog import CatalogDao
from app.core.Response import ResponseDto, ListResponseDto
from app.schema.http.api.api_in import ApiCreateBody, ApiUpdateBody, SingleApiRunBody
from ext.httprunning import HttpRunning

router = APIRouter(prefix="/api")


@router.get("/list")
async def list_api(project_id: int, catalog_id="", status="", level="", search="", page: int = 1,
                   limit: int = 10, user_info=Depends(Permission())):
    total, apis = await ApiDao.list(project_id, catalog_id, status, level, search, page, limit)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=apis)


@router.post("/create")
async def create_api(api: ApiCreateBody, user_info=Depends(Permission())):
    fullname = user_info.get("fullname", "系统")
    await ApiDao.create(api, fullname)
    return ResponseDto(msg="创建成功")


@router.get("/{pk}")
async def get_api_detail(pk: int, user_info=Depends(Permission())):
    api = await ApiDao.detail(pk=pk)
    catalog = await CatalogDao.detail(api.catalog_id)
    api.body = json.loads(api.body)
    return ResponseDto(data=dict(api=api, catalog=catalog))


@router.delete("/delete/{pk}")
async def delete_api(pk: int, user_info=Depends(Permission())):
    await ApiDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.put("/update")
async def update_api(api: ApiUpdateBody, user_info=Depends(Permission())):
    fullname = user_info.get("fullname", "系统")
    await ApiDao.update(api, fullname)
    return ResponseDto(msg="更新成功")


@router.post("/run")
async def run_apis(single_api: SingleApiRunBody):
    api = await ApiDao.get_detail_with_id(pk=single_api.api_id)
    config = await ConfigDao.get_detail_with_id(pk=single_api.config_id)
    http_run = HttpRunning([[api.to_dict()]], config.to_dict())
    summary = http_run.run_testcase()
    return ResponseDto(data=summary)


@router.get("/run/result")
async def result():
    return ResponseDto(data=aaa)
