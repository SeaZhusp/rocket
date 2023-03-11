from app.base.curd import BaseCurd
from app.models.http.envconfig import EnvConfig


class EnvConfigFacade(BaseCurd):
    model = EnvConfig

    @classmethod
    async def get_detail_with_id(cls, pk):
        return cls.get_with_id(pk=pk)
