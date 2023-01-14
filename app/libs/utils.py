import hashlib

from app.core.Exceptions import ParamsError


class StringUtil(object):

    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ParamsError("不能为空")
        return v

    @staticmethod
    def to_md5(v):
        m = hashlib.md5()
        m.update(v.encode("utf-8"))
        return m.hexdigest()
