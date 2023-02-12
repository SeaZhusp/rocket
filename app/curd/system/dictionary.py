from sqlalchemy import and_, or_

from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.system.dictionary import Dict, DictItem


class DictDao(BaseCurd):
    model = Dict

    @classmethod
    async def list(cls, page: int = 1, limit: int = 10, search: str = None):
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
        o = Dict(_dict)
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def delete(cls, pk):
        return cls.delete_with_id(pk=pk)

    @classmethod
    async def update(cls, _dict):
        filter_list = [and_(cls.model.name == _dict.name, cls.model.id != _dict.id)]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("字典已存在")
        o = cls.update_with_id(model=_dict)
        return o


class DictItemDao(BaseCurd):
    model = DictItem

    @classmethod
    async def list(cls, search: int):
        dict_items = cls.get_with_params(dict_id=search, _sort=['sort'], _sort_type='asc')
        return dict_items

    @classmethod
    async def create(cls, dict_item):
        filter_list = [or_(cls.model.value == dict_item.value, cls.model.label == dict_item.label)]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("字典项名或值已存在")
        o = DictItem(dict_item)
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def update(cls, dict_item):
        filter_list = [and_(cls.model.label == dict_item.label, cls.model.value == dict_item.value,
                            cls.model.id != dict_item.id)]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("字典已存在")
        o = cls.update_with_id(model=dict_item)
        return o

    @classmethod
    async def delete(cls, pk):
        return cls.delete_with_id(pk=pk)
