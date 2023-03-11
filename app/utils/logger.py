from loguru import logger

from app.core.exc.exceptions import BusinessException


def log_exception(f):
    exception = f.exception()
    if exception:
        # 如果exception获取到了值，说明有异常.exception就是异常类
        logger.error(f"异步执行出错: f{exception}")
        raise BusinessException(msg=f"{exception}")
