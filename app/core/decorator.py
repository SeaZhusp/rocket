import functools
from loguru import logger
from app.core.exc.exceptions import BusinessException


# 捕获异常装饰器
def exception_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            func_name = func.__doc__
            # func_params = dict(args=args, kwargs=kwargs)
            import traceback
            err = traceback.format_exc()
            logger.error(f"{func_name}失败: {err}")
            raise BusinessException(str(e))

    return wrapper
