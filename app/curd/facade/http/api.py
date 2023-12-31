from app.base.curd import BaseCurd
from app.models.http.api import Api


class ApiFacade(BaseCurd):
    model = Api

    @classmethod
    async def exist_by_catalog_id(cls, catalog_id):
        return cls.get_with_existed(filter_list=[cls.model.catalog_id == catalog_id])

    @classmethod
    async def get_detail_with_id(cls, pk: int):
        return cls.get_with_id(pk=pk)
