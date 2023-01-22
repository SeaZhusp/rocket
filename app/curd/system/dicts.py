from sqlalchemy import and_, or_

from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.system.dicts import Dict


class DictDao(BaseCurd):
    model = Dict

    @classmethod
    async def query_with_name(cls, page: int = 1, limit: int = 10, search: str = None):
        total, dicts = cls.get_with_pagination(page=page, limit=limit, _sort=['create_time'],
                                               name=f"%{search}%" if search else None)
        return total, dicts

    @classmethod
    async def create(cls, _dict):
        filter_list = [or_(cls.model.code == _dict.code,
                           and_(cls.model.name == _dict.name, cls.model.type == _dict.type))]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("字典或编号已存在")
        project = Dict(_dict)
        return cls.insert_with_model(model_obj=project)
