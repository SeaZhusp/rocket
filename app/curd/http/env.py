from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.http.env import Env


class EnvDao(BaseCurd):
    model = Env

    @classmethod
    async def create(cls, env):
        filter_list = [cls.model.name == env.name]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("环境已存在")
        o = Env(**env.dict())
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def list(cls, search, page: int = 1, limit: int = 10):
        return cls.get_with_pagination(page=page, limit=limit, _sort=['create_time'],
                                       name=f"%{search}%" if search else None)
