import importlib
import os
import traceback
import types

from fastapi import APIRouter, Depends

from app.core.Response import ResponseDto
from app.core.Auth import Permission
from app.schema.http.pyshell.pyshell_in import DebugFunctionBody
from app.utils.utils import get_function_from_content, parse_function_meta

router = APIRouter(prefix="/pyshell")

pyshell_path = os.path.join(os.path.abspath("."), "pyshell")


@router.get("/list")
async def list_pyshell(user_info=Depends(Permission())):
    modules = []
    for root, dirs, files in os.walk(pyshell_path):
        modules.extend([{"value": file} for file in files if "__init__.py" != file and file.endswith(".py")])
    return ResponseDto(data=modules)


@router.get("/info")
async def get_func(module_name: str, user_info=Depends(Permission())):
    module = os.path.join(pyshell_path, module_name)
    if not os.path.exists(module):
        return ResponseDto(msg=f"{module_name}不存在")
    with open(module, "r", encoding="utf8") as f:
        content = f.read()
    functions = get_function_from_content(content)
    return ResponseDto(data=dict(content=content, functions=functions))


@router.post("/debug")
async def debug_function(debug_functions: DebugFunctionBody, user_info=Depends(Permission())):
    module_name = debug_functions.module_name
    func_express = debug_functions.func_express
    try:
        import_path = "pyshell.{}".format(module_name.replace(".py", ""))
        func_list = importlib.reload(importlib.import_module(import_path))
        module_functions_dict = {name: item for name, item in vars(func_list).items() if
                                 isinstance(item, types.FunctionType)}
        function_meta = parse_function_meta(func_express)
        return ResponseDto(data=module_functions_dict[function_meta["func_name"]](*function_meta["args"]))
    except:
        error_data = "\n".join("{}".format(traceback.format_exc()).split("↵"))
        return ResponseDto(msg="语法错误，请自行检查", data=error_data)
