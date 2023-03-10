from app.routers.system import user, dictionary, file
from app.routers.http import api, envconfig, pyshell, testcase, plan
from app.routers.manage import project, catalog
from collections import namedtuple

Router = namedtuple("router", ["module", "prefix", "tags"])

router_list = [
    Router(module=user.router, prefix="/sys", tags=["用户管理"]),
    Router(module=dictionary.router, prefix="/sys", tags=["字典管理"]),
    Router(module=file.router, prefix="/sys", tags=["文件管理"]),

    Router(module=project.router, prefix="/manage", tags=["项目管理"]),
    Router(module=catalog.router, prefix="/manage", tags=["目录管理"]),

    Router(module=envconfig.router, prefix="/http", tags=["环境管理"]),
    Router(module=pyshell.router, prefix="/http", tags=["Pyshell"]),
    Router(module=api.router, prefix="/http", tags=["接口测试"]),
    Router(module=testcase.router, prefix="/http", tags=["测试用例"]),
    Router(module=plan.router, prefix="/http", tags=["测试计划"]),

]
