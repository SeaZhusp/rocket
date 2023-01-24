from app.routers.system import user, dictionary, env, project, catalog
from collections import namedtuple

Router = namedtuple('router', ['module', 'prefix', 'tags'])

router_list = [
    Router(module=user.router, prefix='/sys', tags=["用户管理"]),
    Router(module=dictionary.router, prefix='/sys', tags=["字典管理"]),
    Router(module=project.router, prefix='/sys', tags=["项目管理"]),
    Router(module=env.router, prefix='/sys', tags=["环境管理"]),
    Router(module=catalog.router, prefix='/sys', tags=["目录管理"]),
]
