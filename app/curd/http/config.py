from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.http.config import Config


class ConfigDao(BaseCurd):
    model = Config

    @classmethod
    async def create(cls, env):
        filter_list = [cls.model.name == env.name]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("环境已存在")
        o = Config(**env.dict())
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def list(cls, search, page: int = 1, limit: int = 10):
        return cls.get_with_pagination(page=page, limit=limit, _sort=["create_time"],
                                       name=f"%{search}%" if search else None)

    @classmethod
    async def delete(cls, pk):
        cls.delete_with_id(pk=pk)

    @classmethod
    async def update(cls, env):
        return cls.update_with_id(model=env)

    @classmethod
    async def get_detail_with_id(cls, pk):
        return cls.get_with_id(pk=pk)
