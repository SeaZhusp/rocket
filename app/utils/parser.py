import ast
import re
import json
from app.core.enums import ValueTypeEnum
from loguru import logger


def parse_function_from_content(module_content):
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
        return ast.literal_eval(str_value)  # 将字符串（如数字、字符串、元组、列表、字典、布尔值和None）转换对应的 Python 对象
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

    return function_meta


def __format_value(__key, __type, __value):
    """parser list[dict] to dict
        Examples:
            >>> [{"key": "count", "type": 1, "value": "520", "desc": "转为数字"}]
            >>> {"count": 520}
    """
    if __type == ValueTypeEnum.STRING:
        __value = str(__value)
    elif __type == ValueTypeEnum.INT:
        __value = int(__value)
    elif __type == ValueTypeEnum.FLOAT:
        __value = float(__value)
    elif __type == ValueTypeEnum.BOOL:
        __value = bool(__value)
    elif __type == ValueTypeEnum.LIST or __type == ValueTypeEnum.DICT:
        __value = json.loads(__value)
    return {__key: __value}


def parse_2_mapping(items):
    """parser list[dict] to dict
    Examples:
        >>> [{"key": "username", "value": "admin", "desc": "账号"}]
        >>> {"username": "admin"}
    """
    mapping = {}
    for item in items:
        mapping.update({item.get("key"): item.get("value")})
    return mapping


def parse_variables(variables):
    __variables = {}
    for variable in variables:
        __type = variable.get("type")
        __key = variable.get("key")
        __value = variable.get("value")
        __variables.update(__format_value(__key, __type, __value))
    return __variables


def parse_headers(headers):
    return parse_2_mapping(headers)


def parse_request(method, url, params, headers, req):
    __request = {}
    __data_type = req.get("data_type")
    __form_data = req.get("form_data")
    __json_data = req.get("json_data")

    def __parse_form_data(__form_data):
        if __data_type == "json":
            form_data = None
        else:
            form_data = parse_variables(__form_data)
        return form_data

    __data = __parse_form_data(__form_data)

    try:
        __json = json.loads(__json_data)
    except Exception as ex:
        logger.error(
            f"error parse json_data:{__json_data}\n"
            f"{type(ex).__name__}:{ex}")
        __json = {}

    __request = {}
    __request.update(method=method)
    __request.update(url=url)
    __request.update(headers=headers)
    __request.update(params=params)
    __request.update(json=__json)
    __request.update(data=__data)
    __request.update(upload={})
    return __request if __request else None


def parse_extract(extract):
    return parse_2_mapping(extract)


def parse_validate(validates):
    __validates = []
    for validate in validates:
        item = {}
        __actual = validate.get("actual")
        __comparator = validate.get("comparator")
        __type = validate.get("type")
        __expect = validate.get("expect")
        fmt = __format_value(__actual, __type, __expect)
        item[__comparator] = [__actual, fmt.get(__actual)]
        __validates.append(item)
    return __validates


def parse_step(api, config):
    __service_mapping = config.get("service")
    __name = api.get("name")
    __body = json.loads(api.get("body"))
    __service = api.get("service")
    __hooks = __body.get("hooks")

    # variables
    __variables: dict = config.get("variables", {})
    __api_variables = parse_variables(__body.get("variables", [])) if len(__body.get("variables", [])) > 0 else {}
    __api_variables.update(__variables)

    # setup_hooks
    setup_hooks = __hooks.get("setup_hooks")
    __setup_hooks = [setup_hook.get("setup_hook") for setup_hook in setup_hooks if setup_hook]

    # request
    __params = parse_2_mapping(__body.get("params", []))
    __url = __service_mapping.get(__service) + api.get("path")
    __method = api.get("method")
    __headers = config.get("headers", {})
    __api_headers = parse_headers(__body.get("headers", [])) if len(__body.get("headers", [])) > 0 else {}
    __api_headers.update(__headers)
    __request = parse_request(__method, __url, __params, __api_headers, __body.get("request"))

    # teardown_hooks
    teardown_hooks = __hooks.get("teardown_hooks")
    __teardown_hooks = [teardown_hook.get("teardown_hook") for teardown_hook in teardown_hooks if teardown_hook]

    # extract
    __extract = parse_extract(__body.get("extract") if len(__body.get("extract", [])) > 0 else {})

    # todo: export

    # validators
    __validate = parse_validate(__body.get("validator", []))

    # todo: validate_script

    return dict(name=__name,
                variables=__api_variables,
                setup_hooks=__setup_hooks,
                request=__request,
                teardown_hooks=__teardown_hooks,
                extract=__extract,
                validate=__validate)


def parse_curl(curl_command):
    """解析curl"""
    # 提取请求地址
    url_match = re.search(r"'(.*?)'", curl_command)
    url = url_match.group(1)

    # 提取请求头
    headers_match = re.findall(r"-H '(.*?)'", curl_command)
    headers = {}
    for header in headers_match:
        header_parts = header.split(': ')
        key = header_parts[0]
        value = header_parts[1]
        if key not in ['token', 'source', 'content-type']:
            continue
        headers[key] = value

    # 提取请求参数
    data_match = re.search(r"-data-raw '(.*?)'", curl_command)
    data = data_match.group(1)

    return dict(url=url, headers=headers, data=data)
