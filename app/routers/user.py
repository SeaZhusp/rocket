from fastapi import APIRouter, Depends

from app.curd.user import UserDao
from app.core.TokenAuth import UserToken
from app.routers import Permission
from app.schema.user import UserRegisterForm, UserLoginForm
from app.core.response import Response

router = APIRouter(prefix="/user")


@router.post("/create")
async def create(user: UserRegisterForm):
    await UserDao.register_user(user)
    return Response.success(msg='注册成功')


@router.post("/login")
async def login(login_user: UserLoginForm):
    user = await UserDao.login(login_user)
    user_info = Response.model_to_dict(user, "password")
    token = UserToken.generate_token(user_info)
    return Response.success(data=dict(userInfo=user_info, token=token), msg="登录成功")


@router.get('/list')
async def list_user(offset: int = 1, limit: int = 10, user=Depends(Permission())):
    return dict(offset=offset, limit=limit)
