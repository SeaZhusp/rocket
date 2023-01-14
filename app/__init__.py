from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import status
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

rocket = FastAPI()

HTTP_CODE_MSG = {
    404: "请求路径找不到",
    405: "请求方法不支持",
    408: "请求超时",
    500: "服务器内部错误"
}


def error_map(error_type: str, field: str, msg: str = None):
    if "missing" in error_type:
        return f"缺少参数: {field}"
    if "params" in error_type:
        return f"参数: {field} {'不规范' if msg is None else msg}"
    if "not_allowed" in error_type:
        return f"参数: {field} 类型不正确"
    if "type_error" in error_type:
        return f"参数: {field} 类型不合法"


@rocket.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": -1,
            "msg": error_map(exc.errors()[0]["type"], exc.errors()[0].get("loc", ['unknown'])[-1],
                             exc.errors()[0].get("msg")) if len(exc.errors()) > 0 else "参数解析失败",
        })
    )


@rocket.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        content={"code": -1, "msg": HTTP_CODE_MSG.get(exc.status_code, exc.detail), "data": None}
    )


async def global_execution_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(code=-1, msg="unknown error: " + str(exc)),
    )
