import math


class Utils(object):

    @staticmethod
    def get_total_page(total: int, size: int) -> int:
        return math.ceil(total / size)


class StringUtils(object):

    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ValueError("不能为空")
        return v
