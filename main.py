from app import rocket, create_global_exception_handler, register_middlewares, register_routers, init_logging, \
    register_scheduler
from loguru import logger

from config import BANNER, ROCKET_ENV


@rocket.on_event("startup")
async def start_event():
    init_logging()
    logger.info("logging is init success！！！")

    logger.success(f"rocket is running at <red>{ROCKET_ENV}</red>")
    logger.success(BANNER)

    # step1 注册路由
    await register_routers(rocket)
    logger.info("routers is register success！！！")

    # step2 注册中间件
    await register_middlewares(rocket)
    logger.info("middlewares is register success！！！")

    # step3 注册全局异常处理器
    await create_global_exception_handler(rocket)
    logger.info("exceptionHandler is register success！！！")

    from app.models import Base, engine
    # step4 向数据库发出建表完成类与表的映射
    Base.metadata.create_all(engine)
    logger.info("db is init success！！！")

    await register_scheduler(rocket)
    logger.info("ApScheduler started success！！！")

    logger.info("Rocket is start success！！！")
