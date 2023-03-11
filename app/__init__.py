import json

from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.auth import request_context
from app.routers import router_list
from app.core.exc.exceptions import BusinessException, AuthException, PermissionException
from app.core.response import ResponseDto
from app.core.exc.exceptions_handler import business_exception_handler, global_exception_handler, \
    http_exception_handler, validation_exception_handler, auth_exception_handler, permission_exception_handler
from config import LOGGING_CONF

rocket = FastAPI()


async def request_info(request: Request):
    """获取请求流量信息"""
    logger.bind(name=None).info(f"{request.method} {request.url}")
    try:
        from urllib import parse
        log_msg = ""
        params = request.query_params
        body = await request.body()
        headers = request.headers
        if params:
            log_msg += f"路径参数: {parse.unquote(str(params))}"
        if body and "application/json" in headers.get("content-type"):
            try:
                body = json.dumps(json.loads(body), ensure_ascii=False)
                log_msg += f"请求参数: {body}"
            except:
                log_msg += "解析json失败"
        if log_msg:
            logger.bind(payload=body, name=None).info(log_msg)
    except:
        try:
            body = await request.body()
            if len(body) != 0:
                # 有请求体，记录日志
                logger.bind(payload=body, name=None).info(body)
        except:
            # 忽略文件上传类型的数据
            pass


async def register_routers(_app: FastAPI):
    for router in router_list:
        _app.include_router(router.module, prefix=router.prefix, tags=router.tags,
                            dependencies=[Depends(request_context), Depends(request_info)])


async def register_middlewares(_app: FastAPI):
    """注册中间件，注意中间件的注册顺序"""
    # 中间件执行的顺序是，谁先注册，谁就再最内层，它的再后一个注册，就再最外层
    # middleware_list = [ AuthMiddleware, ExceptionMiddleware ]
    # for middleware in middleware_list:
    #     _app.add_middleware(middleware)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def create_global_exception_handler(_app: FastAPI):
    """创建全局异常处理器"""
    exception_handler_list = [(StarletteHTTPException, http_exception_handler),
                              (RequestValidationError, validation_exception_handler),
                              (AuthException, auth_exception_handler),
                              (PermissionException, permission_exception_handler),
                              (BusinessException, business_exception_handler),
                              (Exception, global_exception_handler)
                              ]
    for exception_name, exception_handler in exception_handler_list:
        _app.add_exception_handler(exception_name, exception_handler)


def init_logging(logging_conf=LOGGING_CONF):
    for log_handler, log_conf in logging_conf.items():
        log_file = log_conf.pop("file", None)
        logger.add(log_file, **log_conf)
