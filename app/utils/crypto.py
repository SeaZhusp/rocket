import hashlib


class Crypto(object):

    @staticmethod
    def md5(v):
        m = hashlib.md5()
        m.update(v.encode("utf-8"))
        return m.hexdigest()
