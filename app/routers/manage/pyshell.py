import traceback
from fastapi import APIRouter, Depends
from app.core.enums import DutyEnum
from app.core.response import ResponseDto
from app.core.auth import Auth
from app.curd.manage.pyshell import PyshellDao
from app.schema.manage.pyshell.pyshell_in import DebugFunctionBody, SavePyshellBody, CreatePyshellBody
from app.utils.parser import parse_function_from_content, parse_function_meta
from app.utils.utils import ModuleUtils

router = APIRouter(prefix="/pyshell")


@router.get("/list")
async def list_pyshell(user_info=Depends(Auth())):
    pyshell_list = await PyshellDao.list()
    module_list = []
    module_list.extend([{"value": pyshell.module_name, "id": pyshell.id} for pyshell in pyshell_list])
    return ResponseDto(data=module_list)


@router.get("/info")
async def get_func(module_name: str, user_info=Depends(Auth())):
    pyshell = await PyshellDao.get_pyshell(module_name)
    if not pyshell:
        return ResponseDto(msg=f"{module_name}不存在")
    code = pyshell.code
    try:
        functions = parse_function_from_content(code)
    except:
        functions = []
    return ResponseDto(data=dict(content=code, functions=functions))


@router.post("/debug")
async def debug_function(debug_functions: DebugFunctionBody, user_info=Depends(Auth())):
    module_name = debug_functions.module_name
    func_express = debug_functions.func_express

    pyshell = await PyshellDao.get_pyshell(module_name=module_name)

    try:
        # get_functions_map接受list，所以要转成list
        module_functions_dict = ModuleUtils.get_functions_map([pyshell])
        function_meta = parse_function_meta(func_express)
        result = module_functions_dict[function_meta["func_name"]](*function_meta["args"])
        return ResponseDto(msg="执行成功", data=result)
    except:
        error_data = "\n".join("{}".format(traceback.format_exc()).split("↵"))
        return ResponseDto(msg="语法错误，请自行检查", data=error_data)


@router.post("/create")
async def create_pyshell(pyshell: CreatePyshellBody, user_info=Depends(Auth())):
    await PyshellDao.create(pyshell=pyshell)
    return ResponseDto(msg="创建成功")


@router.put("/save")
async def save_pyshell(pyshell: SavePyshellBody, user_info=Depends(Auth())):
    await PyshellDao.save_pyshell(pyshell)
    return ResponseDto(msg="保存成功")


@router.delete("/delete")
async def delete_pyshell(pyshell: CreatePyshellBody, user_info=Depends(Auth(DutyEnum.admin))):
    module_name = pyshell.module_name
    if module_name == "rocket.py":
        return ResponseDto(msg=f"{module_name}不允许删除")
    await PyshellDao.delete(module_name)
    return ResponseDto(msg="删除成功")
