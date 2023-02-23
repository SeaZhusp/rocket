from httprunner.utils import get_platform


def __get_variables_to_list(config_vars):
    variables_list = []
    for k, v in config_vars.items():
        variables_list.append({"key": k, "value": v})
    return variables_list


def get_summary(test_results):
    summary = {
        "success": True,
        "stat": [{
            "total": len(test_results),
            "success": 0,
            "failed": 0,
            "duration": 0,
            "start_time": "",
            "platform": get_platform()
        }],
        "time": {
            "duration": 0,
            "start_time": ""
        },
        "platform": get_platform(),
        "details": []
    }
    for test_result in test_results:
        if test_result["success"]:
            summary["stat"][0]["success"] += 1
        else:
            summary["stat"][0]["failed"] += 1
        summary["success"] &= test_result["success"]
        config_vars = test_result["in_out"].pop("config_vars")
        test_result["in_out"]["variables_list"] = __get_variables_to_list(config_vars)
        summary["details"].append(test_result)
    return summary
