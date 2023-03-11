from enum import IntEnum, Enum


class DutyEnum(IntEnum):
    member = 0  # 成员
    leader = 1  # 组长
    admin = 2  # 管理员


class StatusEnum(IntEnum):
    disable = 0  # 禁用
    enable = 1  # 启用


class DeleteEnum(IntEnum):
    YES = 1  # 删除
    NO = 0  # 没删除


class ProjectTypeEnum(IntEnum):
    API = 1  # 接口


class CatalogUsedEnum(IntEnum):
    API = 1
    TESTCASE = 2


class ValueTypeEnum(int, Enum):
    STRING = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    LIST = 5
    DICT = 6


class CodeEnum(Enum):
    """编码枚举类"""
    OK = (200, "请求成功")
    PARAMS_ERROR = (1000, "请求参数错误")
    JSON_ERROR = (2000, "json解析失败")
    BUSINESS_ERROR = (3000, "业务处理异常, 请重试")
    HTTP_ERROR = (4000, "HTTP错误")
    SYSTEM_ERROR = (5000, "系统内部错误")
    AUTH_ERROR = (401, "Token认证失败")
    PERMISSION_ERROR = (403, "权限不足, 请联系管理员")

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def msg(self) -> str:
        return self.value[1]
