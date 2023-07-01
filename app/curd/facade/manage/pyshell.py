from app.base.curd import BaseCurd
from app.models.manage.pyshell import Pyshell


class PyshellFacade(BaseCurd):
    model = Pyshell

    @classmethod
    def get_with_modules(cls, modules: list):
        filter_list = [cls.model.module_name.in_(modules)]
        return cls.get_with_params(filter_list=filter_list)
