from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.curd.http.api import ApiDao
from app.curd.http.project import ProjectDao
from app.models.http.catalog import Catalog


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
    async def list(cls, project_id):
        return cls.get_with_params(filter_list=[cls.model.project_id == project_id])

    @classmethod
    async def get_catalog_tree(cls, project_id):
        tree = list()
        source = list()
        tree_dict = dict()
        catalogs = cls.get_with_params(filter_list=[cls.model.project_id == project_id], _sort=["create_time"],
                                       _sort_type="asc")
        for catalog in catalogs:
            source.append(dict(label=catalog.name,
                               id=catalog.id,
                               parent_id=catalog.parent_id,
                               project_id=catalog.project_id,
                               children=list()))
        for item in source:
            tree_dict[item["id"]] = item
        for i in tree_dict:
            if tree_dict[i]["parent_id"]:
                parent_id = tree_dict[i]["parent_id"]
                parent = tree_dict[parent_id]
                parent.setdefault("children", []).append(tree_dict[i])
            else:
                tree.append(tree_dict[i])
        return tree

    @classmethod
    async def delete(cls, pk):
        ant = cls.get_with_existed(parent_id=pk)
        if ant:
            raise BusinessException("存在子目录，不能删除")
        api_ant = await ApiDao.exist_by_catalog_id(pk)
        if api_ant:
            raise BusinessException("目录下存在接口，不能删除")
        return cls.delete_with_id(pk=pk)

    @classmethod
    async def update(cls, catalog):
        return cls.update_with_id(model=catalog)

    @classmethod
    async def detail(cls, pk):
        return cls.get_with_id(pk=pk)
