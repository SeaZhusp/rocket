from starlette.requests import Request


async def request_context(request: Request):
    """ 保存当前request对象到上下文中 """
    REQUEST_CONTEXT.set(request)
