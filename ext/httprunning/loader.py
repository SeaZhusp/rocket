import importlib
import types


def load_module_functions(module) -> Dict[Text, Callable]:
    """ load python module functions.

    Args:
        module: python module

    Returns:
        dict: functions mapping for specified python module

            {
                "func1_name": func1,
                "func2_name": func2
            }

    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


def load_functions(func_file_list):
    functions = {}
    for func_file in func_file_list:
        try:
            imported_module = importlib.import_module("func_folder.{}".format(func_file.replace('.py', '')))
        except Exception as ex:
            raise f"error occurred in {func_file}: {ex}"

        imported_module = importlib.reload(imported_module)
        module_functions = load_module_functions(imported_module)
        functions.update(module_functions)
    return functions
