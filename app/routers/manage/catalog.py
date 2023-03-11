from fastapi import APIRouter, Depends

from app.core.auth import Auth
from app.core.response import ResponseDto
from app.curd.manage.catalog import CatalogDao
from app.schema.http.catalog.catalog_in import CatalogCreateBody, CatalogUpdateBody

router = APIRouter(prefix="/catalog")


@router.post("/create")
async def create_catalog(catalog: CatalogCreateBody, user_info=Depends(Auth())):
    await CatalogDao.create(catalog)
    return ResponseDto(msg="创建成功")


@router.get("/list")
async def list_catalog(used: str, project_id: int, user_info=Depends(Auth())):
    catalogs = await CatalogDao.list(used, project_id)
    return ResponseDto(data=catalogs)


@router.get("/tree")
async def get_catalog_tree(used: str, project_id: int, user_info=Depends(Auth())):
    catalog_tree = await CatalogDao.get_catalog_tree(used, project_id)
    return ResponseDto(data=catalog_tree)


@router.delete("/delete/{pk}")
async def delete_catalog(pk: int, user_info=Depends(Auth())):
    await CatalogDao.delete(pk)
    return ResponseDto(msg="删除成功")


@router.put("/update")
async def update_catalog(catalog: CatalogUpdateBody, user_info=Depends(Auth())):
    await CatalogDao.update(catalog)
    return ResponseDto(msg="更新成功")
