import hashlib
from datetime import timedelta, datetime

import jwt
from jwt.exceptions import ExpiredSignatureError

from config import Config


class UserToken(object):

    @staticmethod
    def generate_token(data):
        new_data = dict({"exp": datetime.utcnow() + timedelta(hours=Config.TOKEN_EXPIRATION)}, **data)
        return jwt.encode(new_data, key=Config.TOKEN_KEY)

    @staticmethod
    def parse_token(token):
        try:
            return jwt.decode(token, key=Config.TOKEN_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise Exception("token已过期, 请重新登录")
