import json
from loguru import logger

from httprunner import HttpRunner
from httprunner.models import TestCase, TConfig, TStep
from ext.httprunning.parser import parse_variables, parse_step, parse_headers, parse_2_mapping, parse_request, \
    parse_extract, parse_validate


class HttpRunning(object):
    tmp_config: dict = {}

    def __init__(self, api_list, config):
        self.api_list = api_list
        self.my_config = config

    def __handle_tmp_config(self):
        # todo: parameters,export,path
        name = self.my_config.get("name")
        __config = json.loads(self.my_config.get("config"))

        __variables = __config.get("variables", [])
        variables = parse_variables(__variables)

        __headers = __config.get("headers", [])
        headers = parse_headers(__headers)

        self.tmp_config["service"] = {item.get("key"): item.get("value") for item in __config.get("service", [])}
        self.tmp_config["variables"] = variables
        self.tmp_config["headers"] = headers
        self.tmp_config["name"] = name
        return self

    # def __handle_step(self, api):
    #     __service_mapping = self.tmp_config.get("service")
    #     ___name = api.get("name")
    #     __body = json.loads(api.get("body"))
    #     ___service = api.get("service")
    #     __hooks = __body.get("hooks")
    #
    #     # variables
    #     __variables: dict = self.tmp_config.get("variables", {})
    #     __variables.update(
    #         parser_variables(__body.get("variables", [])) if len(__body.get("variables", [])) > 0 else {})
    #
    #     # setup_hooks
    #     setup_hooks = __hooks.get("setup_hooks")
    #     __setup_hooks = [setup_hook.get("setup_hook") for setup_hook in setup_hooks if setup_hook]
    #
    #     # request
    #     __params = parser_2_mapping(__body.get("params", []))
    #     __url = "https://" + __service_mapping.get(___service) + api.get("path")
    #     __method = api.get("method")
    #     __headers = self.tmp_config.get("headers", {})
    #     __headers.update(parser_headers(__body.get("headers", [])) if len(__body.get("headers", [])) > 0 else {})
    #     __request = parser_request(__method, __url, __params, __headers, __body.get("request"))
    #
    #     # teardown_hooks
    #     teardown_hooks = __hooks.get("teardown_hooks")
    #     __teardown_hooks = [teardown_hook.get("teardown_hook") for teardown_hook in teardown_hooks if teardown_hook]
    #
    #     # extract
    #     __extract = parser_extract(__body.get("extract") if len(__body.get("extract", [])) > 0 else {})
    #
    #     # todo: export
    #
    #     # validators
    #     __validate = parser_validate(__body.get("validator", []))
    #     # todo: validate_script
    #
    #     # step: TStep
    #     # step.name = ___name
    #     # step.variables = __variables
    #     # step.setup_hooks = __setup_hooks
    #     # step.request = __request
    #     # step.teardown_hooks = __teardown_hooks
    #     # step.extract = __extract
    #     # step.validate = __validate
    #     return self

    def __handle_steps(self):
        test_steps = []
        for __api in self.api_list:
            self.__handle_tmp_config()
            t_step = TStep(**parse_step(__api, self.tmp_config))
            self.tmp_config["name"] = t_step.name
            test_steps.append(t_step)
        return test_steps

    def run_testcase(self):
        test_steps = self.__handle_steps()
        testcase = TestCase(config=TConfig(**self.tmp_config), teststeps=test_steps)
        runner = HttpRunner()
        runner.run_testcase(testcase)
        summary = runner.get_summary()
        return summary

    def run_plan(self):
        pass
