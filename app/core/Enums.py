from enum import IntEnum, Enum


class DutyEnum(IntEnum):
    member = 0  # 成员
    leader = 1  # 组长
    admin = 2  # 管理员


class StatusEnum(IntEnum):
    disable = 0  # 禁用
    enable = 1  # 启用


class DeleteEnum(IntEnum):
    yes = 1  # 删除
    no = 0  # 没删除


class ProjectTypeEnum(IntEnum):
    api = 0  # 接口


class CodeEnum(Enum):
    """编码枚举类"""
    OK = (200, "请求成功")
    HTTP_ERROR = (201, "HTTP错误")
    PARAMS_ERROR = (101, "请求参数错误")
    JSON_ERROR = (102, "json解析失败")
    BUSINESS_ERROR = (110, "系统处理异常, 请重试")
    AUTH_ERROR = (401, "Token认证失败")
    PERMISSION_ERROR = (403, "权限不足, 请联系管理员")
    SYSTEM_ERROR = (500, "系统内部错误, 请重试")

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def msg(self) -> str:
        return self.value[1]
