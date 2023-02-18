import json

from fastapi import APIRouter, Depends

from app.core.Auth import Permission
from app.core.Enums import DutyEnum
from app.curd.system.dictionary import DictDao
from app.curd.system.user import UserDao
from app.core.TokenAuth import UserToken
from app.utils.utils import Utils
from app.schema.system.user.user_in import UserCreateBody, UserLoginBody, UserUpdateBody
from app.core.Response import ListResponseDto, ResponseDto
from app.schema.system.user.user_out import UserDto

router = APIRouter(prefix="/user")


@router.post("/create")
async def create_user(user: UserCreateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await UserDao.create(user)
    return ResponseDto(msg='创建成功')


@router.post("/login")
async def login(login_user: UserLoginBody):
    user = await UserDao.login(login_user)
    # 将类加载数据到模型中
    user_dto = UserDto.from_orm(user)
    # xx.dict()和 dict()返回模型的字段和值的字典
    # 返回表示 dict() 的 JSON 字符串，只有当转换为json，模型里面的编码规则(json_encoders)才生效
    user_json: str = user_dto.json()
    token = UserToken.generate_token(json.loads(user_json))
    dicts = await DictDao.all_dict_items()
    return ResponseDto(data=dict(userInfo=user, token=token, dicts=dicts), msg="登录成功")


@router.get('/list')
async def list_user(page: int = 1, limit: int = 10, search: str = None, user_info=Depends(Permission())):
    total, users = await UserDao.list(page=page, limit=limit, search=search)
    total_page = Utils.get_total_page(total, limit)
    paging = dict(page=page, limit=limit, total=total, total_page=total_page)
    return ListResponseDto(paging=paging, data=users)


@router.delete('/delete/{pk}')
async def delete_user(pk: int, user_info=Depends(Permission(DutyEnum.admin))):
    await UserDao.delete(pk=pk)
    return ResponseDto(msg="删除成功")


@router.put('/update')
async def update_user(user: UserUpdateBody, user_info=Depends(Permission(DutyEnum.admin))):
    await UserDao.update(user)
    return ResponseDto(msg="更新成功")
