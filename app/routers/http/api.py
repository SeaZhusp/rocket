import json

from fastapi import APIRouter, Depends

from app.curd.facade.http.envconfig import EnvConfigFacade
from app.curd.facade.manage.pyshell import PyshellFacade
from app.curd.http.envconfig import EnvConfigDao
from app.utils.utils import ComputerUtils, ModuleUtils
from app.curd.http.api import ApiDao
from app.core.auth import Auth
from app.curd.manage.catalog import CatalogDao
from app.core.response import ResponseDto, ListResponseDto
from app.schema.http.api.api_in import ApiCreateBody, ApiUpdateBody, SingleApiRunBody
from app.libs.http_run import HttpRunning

router = APIRouter(prefix="/api")


@router.get("/list")
async def list_api(project_id: int, catalog_id="", status="", level="", search="", page: int = 1, limit: int = 10,
                   user_info=Depends(Auth())):
    total, apis = await ApiDao.list(project_id, catalog_id, status, level, search, page, limit)
    total_page = ComputerUtils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=apis)


@router.post("/create")
async def create_api(api: ApiCreateBody, user_info=Depends(Auth())):
    fullname = user_info.get("fullname", "系统")
    await ApiDao.create(api, fullname)
    return ResponseDto(msg="创建成功")


@router.get("/{pk}")
async def get_api_detail(pk: int, user_info=Depends(Auth())):
    api = await ApiDao.detail(pk=pk)
    catalog = await CatalogDao.detail(api.catalog_id)
    api.body = json.loads(api.body)
    return ResponseDto(data=dict(api=api, catalog=catalog))


@router.delete("/delete/{pk}")
async def delete_api(pk: int, user_info=Depends(Auth())):
    await ApiDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.put("/update")
async def update_api(api: ApiUpdateBody, user_info=Depends(Auth())):
    fullname = user_info.get("fullname", "系统")
    await ApiDao.update(api, fullname)
    return ResponseDto(msg="更新成功")


@router.post("/run")
async def run_apis(single_api: SingleApiRunBody, user_info=Depends(Auth())):
    api = await ApiDao.get_detail_with_id(pk=single_api.api_id)
    config_map = await EnvConfigFacade.get_and_parse_config(pk=single_api.env_id)
    http_run = HttpRunning([{"case_id": api.id, "testcase": [api.to_dict()]}], config_map)
    summary = http_run.run_testcase()
    return ResponseDto(data=summary)
