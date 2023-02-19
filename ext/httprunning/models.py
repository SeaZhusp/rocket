from enum import Enum


class ValueTypeEnum(int, Enum):
    STRING = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    LIST = 5
    DICT = 6
