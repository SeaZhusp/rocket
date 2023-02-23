import json

from ext.httprunning.models import ValueTypeEnum
from loguru import logger


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
