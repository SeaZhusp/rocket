from app.base.curd import BaseCurd
from app.models.http.envconfig import EnvConfig
from app.models.http.testplan import Testplan


class TestplanDao(BaseCurd):
    model = Testplan

    @classmethod
    async def list(cls, project_id: int, status="", search="", page: int = 1, limit: int = 10):
        kwargs = {}
        if status != "":
            kwargs.update(status=status)
        if project_id != "":
            kwargs.update(project_id=project_id)
        if search != "":
            kwargs.update(name=f"%{search}%")
        # total, apis = cls.get_with_pagination(page=page, limit=limit, _sort=["create_time"], **kwargs)
        total, apis = cls.get_with_join(page=page, limit=limit, query_fields=[EnvConfig.name],
                                        join_con=[EnvConfig, EnvConfig.id == Testplan.env_id])
        return total, apis

    @classmethod
    async def create(cls, testplan):
        o = Testplan(**testplan.dict())
        cls.insert_with_model(model_obj=o)

    @classmethod
    async def update(cls, testplan):
        return cls.update_with_id(model=testplan)

    @classmethod
    async def delete(cls, pk: int):
        cls.delete_with_id(pk=pk)
