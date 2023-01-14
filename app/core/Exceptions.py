from typing import Any
from fastapi import HTTPException

from app.core.Enums import CodeEnum


class ParamsError(ValueError):
    pass


class BusinessException(Exception):
    """业务异常处理类"""

    def __init__(self, msg: str = CodeEnum.BUSINESS_ERROR.msg) -> None:
        self.code = CodeEnum.BUSINESS_ERROR.code
        self.msg = msg


class NormalException(HTTPException):
    def __init__(self, status_code=200, detail: Any = None) -> None:
        super().__init__(status_code=status_code, detail=detail)


class AuthException(HTTPException):
    def __init__(self, status_code=200, detail: Any = None) -> None:
        super().__init__(status_code=status_code, detail=detail)


class PermissionException(HTTPException):
    def __init__(self, status_code=200, detail: Any = None) -> None:
        super().__init__(status_code=status_code, detail=detail)
