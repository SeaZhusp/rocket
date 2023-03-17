from app.base.curd import BaseCurd
from app.curd.facade.http.api import ApiFacade
from app.utils.utils import CurdUtil
from app.models.manage.catalog import Catalog
from app.curd.manage.project import ProjectDao
from app.core.exc.exceptions import BusinessException


class CatalogDao(BaseCurd):
    model = Catalog

    @classmethod
    async def create(cls, catalog):
        ant = await ProjectDao.exist_by_id(catalog.project_id)
        if not ant:
            raise BusinessException("项目不存在")
        if catalog.parent_id:
            parent_o = cls.get_with_existed(filter_list=[cls.model.id == catalog.parent_id])
            if not parent_o:
                raise BusinessException("父级目录不存在")
        o = Catalog(**catalog.dict())
        cls.insert_with_model(model_obj=o)

    @classmethod
    async def list(cls, used, project_id):
        return cls.get_with_params(project_id=project_id, used=used)

    @classmethod
    async def get_catalog_tree(cls, used, project_id):
        catalogs = cls.get_with_params(used=used, project_id=project_id, _sort=["create_time"], _sort_type="asc")
        tree = CurdUtil.parse_2_tree(catalogs)
        return tree

    @classmethod
    async def get_catalog_tree_with_ids(cls, ids, used: int, project_id: int):
        all_catalogs = cls.get_with_params(used=used, project_id=project_id, _sort=["create_time"], _sort_type="asc")
        catalogs = cls.get_with_params(filter_list=[Catalog.id.in_(ids)])
        catalogs = CurdUtil.recursive_parent_catalog(catalogs, all_catalogs)
        tree = CurdUtil.parse_2_tree(catalogs)
        return tree

    @classmethod
    async def delete(cls, pk):
        ant = cls.get_with_existed(parent_id=pk)
        if ant:
            raise BusinessException("存在子目录，不能删除")
        api_ant = await ApiFacade.exist_by_catalog_id(pk)
        if api_ant:
            raise BusinessException("目录下存在接口，不能删除")
        return cls.delete_with_id(pk=pk)

    @classmethod
    async def update(cls, catalog):
        return cls.update_with_id(model=catalog)

    @classmethod
    async def detail(cls, pk):
        return cls.get_with_id(pk=pk)
