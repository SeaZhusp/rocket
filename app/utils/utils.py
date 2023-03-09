import ast
import math
import re


class StringUtils(object):
    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ValueError("不能为空")
        return v


class ComputerUtils(object):
    @staticmethod
    def get_total_page(total: int, size: int) -> int:
        return math.ceil(total / size)


def get_function_from_content(module_content):
    function_regex_compile = re.compile(r"def\s([\w]*\(.*?\)):")
    functions = function_regex_compile.findall(module_content)
    return [{"value": function} for function in functions]


def parse_string_value(str_value):
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def parse_function_meta(function_express):
    """ parse function name and args from string content.

    Args:
        function_express (str): string content

    Returns:
        dict: function meta dict

            {
                "func_name": "xxx",
                "args": [],
                "kwargs": {}
            }

    Examples:
        >>> parse_function("func()")
        {"func_name": "func", "args": [], "kwargs": {}}

        >>> parse_function("func(5)")
        {"func_name": "func", "args": [5], "kwargs": {}}

        >>> parse_function("func(1, 2)")
        {"func_name": "func", "args": [1, 2], "kwargs": {}}

        >>> parse_function("func(a=1, b=2)")
        {"func_name": "func", "args": [], "kwargs": {"a": 1, "b": 2}}

        >>> parse_function("func(1, 2, a=3, b=4)")
        {"func_name": "func", "args": [1, 2], "kwargs": {"a":3, "b":4}}

    """
    function_regexp_compile = re.compile(r"^([\w_]+)\(([\$\w\.\-/_ =,\"\']*)\)$")
    matched = function_regexp_compile.match(function_express)
    function_meta = {
        "func_name": matched.group(1),
        "args": [],
        "kwargs": {}
    }
    args_str = matched.group(2).strip()
    if args_str == "":
        return function_meta

    args_list = args_str.split(",")
    for arg in args_list:
        arg = arg.strip()
        if "=" in arg:
            key, value = arg.split("=")
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    print(function_meta)
    return function_meta
