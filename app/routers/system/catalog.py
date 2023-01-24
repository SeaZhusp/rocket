from fastapi import APIRouter

from app.core.Response import ResponseDto
from app.curd.system.catalog import CatalogDao
from app.schema.system.catalog.catalog_in import CatalogCreateBody, CatalogUpdateBody

router = APIRouter(prefix='/catalog')


@router.post('/create')
async def create(catalog: CatalogCreateBody):
    await CatalogDao.create(catalog)
    return ResponseDto(msg="创建成功")


@router.get('/list')
async def list_catalog(project_id: int):
    catalogs = await CatalogDao.list(project_id)
    return ResponseDto(data=catalogs)


@router.get('/tree')
async def get_catalog_tree(project_id: int):
    catalog_tree = await CatalogDao.get_catalog_tree(project_id)
    return ResponseDto(data=catalog_tree)


@router.delete('/delete/{ident}')
async def delete(ident: int):
    await CatalogDao.delete_by_id(ident)
    return ResponseDto(msg='删除成功')


@router.put('/update')
async def update(catalog: CatalogUpdateBody):
    await CatalogDao.update(catalog)
    return ResponseDto(msg='更新成功')
