import json

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.Enums import CodeEnum
from app.core.exc.exceptions import BusinessException, PermissionException, AuthException
from app.core.Response import ResponseDto
from config import HTTP_MSG_MAP


# 自定义http异常处理器
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    res = ResponseDto(code=CodeEnum.HTTP_ERROR.code, msg=HTTP_MSG_MAP.get(exc.status_code, exc.detail))
    return JSONResponse(content=res.dict())


# 请求参数校验异常处理器
async def body_validation_exception_handler(request: Request, err: RequestValidationError):
    message = ""
    data = {}
    for raw_error in err.raw_errors:
        if isinstance(raw_error.exc, ValidationError):
            exc = raw_error.exc
            if hasattr(exc, 'model'):
                fields = exc.model.__dict__.get('__fields__')
                for field_key in fields.keys():
                    field_title = fields.get(field_key).field_info.title
                    data[field_key] = field_title if field_title else field_key
            for error in exc.errors():
                field = str(error.get('loc')[-1])
                _msg = error.get("msg")
                message += f"{data.get(field, field)}{_msg},"
        elif isinstance(raw_error.exc, json.JSONDecodeError):
            message += 'json解析失败! '
    res = ResponseDto(code=CodeEnum.PARAMS_ERROR.code, msg=f"请求参数非法!{message[:-1]}")
    return JSONResponse(content=res.dict())


async def business_exception_handler(request: Request, exc: BusinessException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.dict())


# 权限异常处理器
async def permission_exception_handler(request: Request, exc: PermissionException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.dict())


# 用户登录态异常处理处理器
async def auth_exception_handler(request: Request, exc: AuthException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.dict())


async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, PermissionException):
        return await permission_exception_handler(request, exc)
    elif isinstance(exc, AuthException):
        return await auth_exception_handler(request, exc)
    # elif isinstance(exc, ValidationError):
    #     return await res_validation_exception_handler(request, exc)
    else:
        import traceback
        logger.exception(traceback.format_exc())
        res = ResponseDto(code=CodeEnum.SYSTEM_ERROR.code, msg=CodeEnum.SYSTEM_ERROR.msg)
        return JSONResponse(content=res.dict())
