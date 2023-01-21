from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.system.env import Env, Domain


class EnvDao(BaseCurd):
    model = Env

    @classmethod
    async def create(cls, env):
        filter_list = [cls.model.name == env.name]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("项目已存在")
        env = Env(env)
        return cls.insert_with_model(model_obj=env)

    @classmethod
    async def create_env_domain(cls, domain):
        domain = Domain(domain)
        return cls.insert_with_model(model_obj=domain)
