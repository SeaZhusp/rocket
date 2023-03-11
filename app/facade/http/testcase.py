from app.base.curd import BaseCurd
from app.models.http.testcase import Testcase


class TestcaseFacade(BaseCurd):
    model = Testcase

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
