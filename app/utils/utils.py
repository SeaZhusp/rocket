import math


class Utils(object):

    @staticmethod
    def get_total_page(total: int, size: int) -> int:
        return math.ceil(total / size)
