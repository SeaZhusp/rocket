import json
from app.base.curd import BaseCurd
from app.curd.facade.manage.pyshell import PyshellFacade
from app.models.http.envconfig import EnvConfig
from app.utils.utils import ModuleUtils


class EnvConfigFacade(BaseCurd):
    model = EnvConfig

    @classmethod
    async def get_detail_with_id(cls, pk):
        return cls.get_with_id(pk=pk)

    @classmethod
    async def get_and_parse_config(cls, pk):
        config = cls.get_with_id(pk=pk)
        modules = json.loads(config.modules or [])
        pyshell_list = PyshellFacade.get_with_modules(modules)
        functions = ModuleUtils.get_functions_map(pyshell_list)
        config_map = config.to_dict()
        config_map["functions"] = functions
        return config_map
