from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.manage.pyshell import Pyshell


class PyshellDao(BaseCurd):
    model = Pyshell

    @classmethod
    async def list(cls):
        return cls.get_with_params()

    @classmethod
    async def info(cls, pyshell_id):
        return cls.get_with_id(pk=pyshell_id)

    @classmethod
    async def create(cls, pyshell):
        ant = cls.get_with_existed(module_name=pyshell.module_name)
        if ant:
            raise BusinessException("pyshell不存在")
        o = Pyshell(**pyshell.dict())
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def get_pyshell(cls, module_name):
        return cls.get_with_first(module_name=module_name)

    @classmethod
    async def save_pyshell(cls, pyshell):
        filter_list = [cls.model.module_name == pyshell.module_name]
        return cls.update_by_map(filter_list=filter_list, module_name=pyshell.module_name, code=pyshell.code)

    @classmethod
    async def delete(cls, module_name):
        filter_list = [cls.model.module_name == module_name]
        return cls.delete_with_params(filter_list=filter_list)
