from app.base.curd import BaseCurd
from app.core.enums import CatalogUsedEnum
from app.curd.facade.manage.catalog import CatalogFacade
from app.models.http.api import Api
from app.schema.http.api.api_out import ApiDto
from app.utils.utils import CurdUtil


class ApiDao(BaseCurd):
    model = Api

    @classmethod
    async def create(cls, api, create_user):
        api.create_user = create_user
        api.update_user = create_user
        o = Api(**api.dict())
        cls.insert_with_model(model_obj=o)

    @classmethod
    async def list(cls, project_id, catalog_id, status, level, search, page, limit):
        kwargs = {}
        filter_list = []
        if status != "":
            kwargs.update(status=status)
        if level != "":
            kwargs.update(level=level)
        if catalog_id != "":
            all_catalogs = await CatalogFacade.list(CatalogUsedEnum.API, project_id)
            ids = CurdUtil.recursive_child_with_catalog_id(int(catalog_id), all_catalogs)
            filter_list.append(Api.catalog_id.in_(ids))
        if search != "":
            kwargs.update(name=f"%{search}%")
        total, apis = cls.get_with_pagination(filter_list=filter_list, page=page, limit=limit, _fields=ApiDto,
                                              _sort=["create_time"], project_id=project_id, **kwargs)
        return total, apis

    @classmethod
    async def detail(cls, pk):
        return cls.get_with_id(pk=pk)

    @classmethod
    async def delete(cls, pk: int):
        cls.delete_with_id(pk=pk)

    @classmethod
    async def update(cls, api, update_user):
        api.update_user = update_user
        return cls.update_with_id(model=api)

    @classmethod
    async def get_detail_with_id(cls, pk: int):
        return cls.get_with_id(pk=pk)
