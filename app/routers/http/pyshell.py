import os
import types
import importlib
import traceback

from fastapi import APIRouter, Depends

from app.core.enums import DutyEnum
from app.core.response import ResponseDto
from app.core.auth import Auth
from app.schema.http.pyshell.pyshell_in import DebugFunctionBody, CreatePyshellBody, SavePyshellBody
from app.utils.parser import parse_function_from_content, parse_function_meta

router = APIRouter(prefix="/pyshell")

pyshell_path = os.path.join(os.path.abspath("."), "pyshell")


@router.get("/list")
async def list_pyshell(user_info=Depends(Auth())):
    modules = []
    for root, dirs, files in os.walk(pyshell_path):
        modules.extend([{"value": file} for file in files if "__init__.py" != file and file.endswith(".py")])
    return ResponseDto(data=modules)


@router.get("/info")
async def get_func(module_name: str, user_info=Depends(Auth())):
    module = os.path.join(pyshell_path, module_name)
    if not os.path.exists(module):
        return ResponseDto(msg=f"{module_name}不存在")
    with open(module, "r", encoding="utf8") as f:
        content = f.read()
    functions = parse_function_from_content(content)
    return ResponseDto(data=dict(content=content, functions=functions))


@router.post("/debug")
async def debug_function(debug_functions: DebugFunctionBody, user_info=Depends(Auth())):
    module_name = debug_functions.module_name
    func_express = debug_functions.func_express
    try:
        import_path = "pyshell.{}".format(module_name.replace(".py", ""))
        func_list = importlib.reload(importlib.import_module(import_path))
        module_functions_dict = {name: item for name, item in vars(func_list).items() if
                                 isinstance(item, types.FunctionType)}
        function_meta = parse_function_meta(func_express)
        result = module_functions_dict[function_meta["func_name"]](*function_meta["args"])
        return ResponseDto(msg="执行成功", data=result)
    except:
        error_data = "\n".join("{}".format(traceback.format_exc()).split("↵"))
        return ResponseDto(msg="语法错误，请自行检查", data=error_data)


@router.post("/create")
async def create_pyshell(pyshell: CreatePyshellBody, user_info=Depends(Auth())):
    module_name = pyshell.module_name
    if module_name.find(".py") == -1:
        return ResponseDto(msg="请创建正确格式的py文件")
    module = os.path.join(pyshell_path, module_name)
    if os.path.exists(module):
        return ResponseDto(msg="pyshell已存在")
    with open(module, "w", encoding="utf8") as f:
        pass
    return ResponseDto(msg="创建成功")


@router.put("/save")
async def save_pyshell(pyshell_meta: SavePyshellBody, user_info=Depends(Auth())):
    content = pyshell_meta.content
    module_name = pyshell_meta.module_name
    module = os.path.join(pyshell_path, module_name)
    if not os.path.exists(module):
        return ResponseDto(msg=f"{module_name}不存在")
    with open(module, 'w', encoding='utf8') as f:
        f.write(content)
    return ResponseDto(msg="保存成功")


@router.delete("/delete")
async def delete_pyshell(pyshell: CreatePyshellBody, user_info=Depends(Auth(DutyEnum.admin))):
    module_name = pyshell.module_name
    module = os.path.join(pyshell_path, module_name)
    if module_name == "rocket.py":
        return ResponseDto(msg=f"{module_name}不允许删除")
    if not os.path.exists(module):
        return ResponseDto(msg=f"{module_name}不存在")
    os.remove(module)
    return ResponseDto(msg="删除成功")
