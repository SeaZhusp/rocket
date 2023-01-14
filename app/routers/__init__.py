from fastapi import Header
from starlette import status

from app.core.Exceptions import AuthException, PermissionException
from app.core.response import Response
from app.curd.user import UserDao
from app.core.TokenAuth import UserToken
from app.core.Enums import DataPermissionEnum

FORBIDDEN = '对不起，你没有足够的权限'


class Permission:

    def __init__(self, data_permission: int = DataPermissionEnum.member.value):
        self.data_permission = data_permission

    async def __call__(self, token: str = Header(...)):
        if not token:
            raise AuthException(detail="Token认证失败，请检查")
        try:
            user_info = UserToken.parse_token(token)
            if user_info.get("data_permission", 0) < self.data_permission:
                raise PermissionException(status.HTTP_200_OK, FORBIDDEN)
            user = await UserDao.get_user_by_id(user_info['id'])
            if user is None:
                raise Exception("用户不存在")
            user_info = Response.model_to_dict(user, "password")
        except PermissionException as e:
            raise e
        except Exception as e:
            raise AuthException(status.HTTP_200_OK, detail='token认证失败,请重新登录')
        return user_info
