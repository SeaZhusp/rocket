import json

from ext.httprunning.loader import load_functions
from httprunner import HttpRunner
from httprunner.models import TestCase, TConfig, TStep, ProjectMeta
from ext.httprunning.parser import parse_variables, parse_step, parse_headers


class HttpRunning(object):

    def __init__(self, testcases, config):
        self.testcases = testcases
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

    def __handle_steps(self, testcase, config):
        steps = []
        for __api in testcase:
            self.__handle_tmp_config()
            step = TStep(**parse_step(__api, config))
            steps.append(step)
        return steps

    def __handle_testcase(self, testcase, config):
        test_steps = self.__handle_steps(testcase, config)
        h_testcase = TestCase(config=TConfig(**config), teststeps=test_steps)
        return h_testcase

    def run_testcase(self):
        config = self.__handle_tmp_config()
        functions = load_functions()
        summary = []
        for testcase in self.testcases:
            h_testcase = self.__handle_testcase(testcase, config)
            runner = HttpRunner().with_project_meta(ProjectMeta(functions=functions))
            runner.run_testcase(h_testcase)
            summary.append(runner.get_summary())
        return summary
