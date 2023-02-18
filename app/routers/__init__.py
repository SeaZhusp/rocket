from app.routers.system import user, dictionary, project, catalog, file
from app.routers.http import api, env
from collections import namedtuple

Router = namedtuple('router', ['module', 'prefix', 'tags'])

router_list = [
    Router(module=user.router, prefix='/sys', tags=["用户管理"]),
    Router(module=dictionary.router, prefix='/sys', tags=["字典管理"]),
    Router(module=project.router, prefix='/sys', tags=["项目管理"]),
    Router(module=catalog.router, prefix='/sys', tags=["目录管理"]),
    Router(module=file.router, prefix='/sys', tags=['文件管理']),

    Router(module=api.router, prefix='/http', tags=['接口测试']),
    Router(module=env.router, prefix='/http', tags=["环境管理"]),

]
