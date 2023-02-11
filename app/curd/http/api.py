from app.base.curd import BaseCurd
from app.models.http.api import Api
from app.schema.http.api.api_out import ApiDto


class ApiDao(BaseCurd):
    model = Api

    @classmethod
    async def create(cls, api, create_user):
        api.create_user = create_user
        api.update_user = create_user
        o = Api(**api.dict())
        cls.insert_with_model(model_obj=o)

    @classmethod
    async def list(cls, project_id: int, catalog_id="", status="", level="", search="", page: int = 1,
                   limit: int = 10):
        kwargs = {}
        if status != "":
            kwargs.update(status=status)
        if level != "":
            kwargs.update(level=level)
        if catalog_id != "":
            kwargs.update(catalog_id=catalog_id)
        if search != "":
            kwargs.update(name=f"%{search}%")
        total, apis = cls.get_with_pagination(page=page, limit=limit, _fields=ApiDto, _sort=['create_time'],
                                              project_id=project_id, **kwargs)
        return total, apis
