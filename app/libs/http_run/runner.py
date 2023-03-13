import json
import time

from app.utils.loader import load_functions
from app.libs.http_run.report import get_summary
from httprunner import HttpRunner
from httprunner.models import TestCase, TConfig, TStep, ProjectMeta
from app.utils.parser import parse_variables, parse_step, parse_headers


class HttpRunning(object):

    def __init__(self, testcases, config):
        self.testcases = testcases
        self.my_config = config

    def __handle_tmp_config(self):
        # todo: parameters,export,path
        config = {}
        __config = json.loads(self.my_config.get("config"))

        __variables = __config.get("variables", [])
        variables = parse_variables(__variables)

        __headers = __config.get("headers", [])
        headers = parse_headers(__headers)

        config["service"] = {item.get("key"): item.get("value") for item in __config.get("service", [])}
        config["variables"] = variables
        config["headers"] = headers
        return config

    def __handle_steps(self, testcase, config):
        steps = []
        for __api in testcase:
            config["name"] = __api.get("name")
            self.__handle_tmp_config()
            step = TStep(**parse_step(__api, config))
            steps.append(step)
        return steps

    def __handle_testcase(self, testcase, config):
        test_steps = self.__handle_steps(testcase, config)
        h_testcase = TestCase(config=TConfig(**config), teststeps=test_steps)
        return h_testcase

    def run_testcase(self):
        start_at = time.strftime("%Y-%m-%d %H:%M:%S")
        start_time = time.time()
        config = self.__handle_tmp_config()
        functions = load_functions()
        test_results = []
        for testcase in self.testcases:
            # parse_case_at = time.time()
            h_testcase = self.__handle_testcase(testcase["testcase"], config)
            # parse_case_use = round(time.time() - parse_case_at, 2)
            # http_run_at = time.time()
            runner = HttpRunner() \
                .with_project_meta(ProjectMeta(functions=functions)) \
                .with_case_id(case_id=testcase["case_id"])
            runner.run_testcase(h_testcase)
            # http_run__use = round(time.time() - parse_case_at, 2)
            test_results.append(runner.get_summary().dict())
        # gen_summary_at = time.time()
        summary = get_summary(test_results)
        summary["stat"][0]["duration"] = round(time.time() - start_time, 3)
        summary["stat"][0]["start_time"] = start_at
        # gen_summary_use = round(time.time() - gen_summary_at, 2)

        return summary
