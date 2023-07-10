from app.core.enums import CodeEnum


class BusinessException(Exception):
    """业务异常处理类"""

    def __init__(self, msg: str = CodeEnum.BUSINESS_ERROR.msg) -> None:
        self.code = CodeEnum.BUSINESS_ERROR.code
        self.msg = msg


class AuthException(BusinessException):
    """登录态异常类"""

    def __init__(self, msg: str = CodeEnum.AUTH_ERROR.msg) -> None:
        self.code = CodeEnum.AUTH_ERROR.code
        self.msg = msg


class PermissionException(BusinessException):
    """用户权限不足异常类"""

    def __init__(self) -> None:
        self.code = CodeEnum.PERMISSION_ERROR.code
        self.msg = CodeEnum.PERMISSION_ERROR.msg
