import json

from httprunner import HttpRunner
from httprunner.models import TestCase, TConfig, TStep
from ext.httprunning.parser import parse_variables, parse_step, parse_headers


class HttpRunning(object):

    def __init__(self, api_list, config):
        self.api_list = api_list
        self.my_config = config

    def __handle_tmp_config(self):
        # todo: parameters,export,path
        config = {}
        name = self.my_config.get("name")
        __config = json.loads(self.my_config.get("config"))

        __variables = __config.get("variables", [])
        variables = parse_variables(__variables)

        __headers = __config.get("headers", [])
        headers = parse_headers(__headers)

        config["service"] = {item.get("key"): item.get("value") for item in __config.get("service", [])}
        config["variables"] = variables
        config["headers"] = headers
        config["name"] = name
        return config

    def __handle_steps(self, config):
        steps = []
        for __api in self.api_list:
            self.__handle_tmp_config()
            step = TStep(**parse_step(__api, config))
            steps.append(step)
        return steps

    def __handle_testcase(self):
        config = self.__handle_tmp_config()
        test_steps = self.__handle_steps(config)
        testcase = TestCase(config=TConfig(**config), teststeps=test_steps)
        return testcase

    def run_testcase(self):
        testcase = self.__handle_testcase()
        runner = HttpRunner()
        runner.run_testcase(testcase)
        summary = runner.get_summary()
        return summary
