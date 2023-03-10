from app.base.curd import BaseCurd
from app.core.Enums import CatalogUsedEnum
from app.facade.manage.catalog import CatalogFacade
from app.models.http.testcase import Testcase
from app.utils.utils import CurdUtil


class TestcaseDao(BaseCurd):
    model = Testcase

    @classmethod
    async def list(cls, project_id: int, catalog_id="", status="", level="", search="", page: int = 1, limit: int = 10):
        kwargs = {}
        filter_list = []
        if status != "":
            kwargs.update(status=status)
        if level != "":
            kwargs.update(level=level)
        if catalog_id != "":
            all_catalogs = await CatalogFacade.list(CatalogUsedEnum.TESTCASE, project_id)
            ids = CurdUtil.recursive_child_with_catalog_id(int(catalog_id), all_catalogs)
            filter_list.append(Testcase.catalog_id.in_(ids))
        if search != "":
            kwargs.update(name=f"%{search}%")
        total, testcases = cls.get_with_pagination(filter_list=filter_list, page=page, limit=limit,
                                                   _sort=["create_time"], project_id=project_id, **kwargs)
        return total, testcases

    @classmethod
    async def create(cls, testcase, create_user):
        testcase.create_user = create_user
        testcase.update_user = create_user
        o = Testcase(**testcase.dict())
        cls.insert_with_model(model_obj=o)

    @classmethod
    async def update(cls, testcase, update_user):
        testcase.update_user = update_user
        return cls.update_with_id(model=testcase)

    @classmethod
    async def delete(cls, pk: int):
        cls.delete_with_id(pk=pk)

    @classmethod
    async def get_detail_with_id(cls, pk: int):
        return cls.get_with_id(pk=pk)

    @classmethod
    async def list_all_by_ids(cls, ids):
        return cls.get_with_params(filter_list=[Testcase.id.in_(ids)])

    @classmethod
    async def list_by_ids_with_condition(cls, ids, catalog_id="", page: int = 1, limit: int = 10):
        kwargs = {}
        if catalog_id != "":
            kwargs.update(catalog_id=catalog_id)
        total, testcases = cls.get_with_pagination(filter_list=[Testcase.id.in_(ids)], page=page, limit=limit, **kwargs)
        return total, testcases
