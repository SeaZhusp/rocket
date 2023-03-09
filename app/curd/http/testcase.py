from app.base.curd import BaseCurd
from app.models.http.testcase import Testcase


class TestcaseDao(BaseCurd):
    model = Testcase

    @classmethod
    async def list(cls, project_id: int, catalog_id="", status="", level="", search="", page: int = 1, limit: int = 10):
        kwargs = {}
        if status != "":
            kwargs.update(status=status)
        if level != "":
            kwargs.update(level=level)
        if catalog_id != "":
            kwargs.update(catalog_id=catalog_id)
        if search != "":
            kwargs.update(name=f"%{search}%")
        total, testcases = cls.get_with_pagination(page=page, limit=limit, _sort=["create_time"], project_id=project_id,
                                                   **kwargs)
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
