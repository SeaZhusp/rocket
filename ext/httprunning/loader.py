import importlib
import types
from loguru import logger


def load_module_functions(module):
    module_functions = {}
    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions


def load_functions(func_file_list=None):
    builtin = ["rocket.py"]
    if (func_file_list is None) or (not isinstance(func_file_list, list)):
        logger.warning(f"Warring: func_file_list is None or not list type, thus, set func_file_list=[]")
        func_file_list = []
    functions = {}
    func_file_list.extend(builtin)
    for func_file in func_file_list:
        try:
            imported_module = importlib.import_module("pyshell.{}".format(func_file.replace(".py", "")))
        except Exception as ex:
            raise f"error occurred in {func_file}: {ex}"
        imported_module = importlib.reload(imported_module)
        module_functions = load_module_functions(imported_module)
        functions.update(module_functions)
    return functions
