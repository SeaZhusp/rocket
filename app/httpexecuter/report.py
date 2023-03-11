from httprunner.utils import get_platform


def __get_variables_to_list(config_vars):
    variables_list = []
    for k, v in config_vars.items():
        variables_list.append({"key": k, "value": v})
    return variables_list


def get_summary(test_results):
    summary = {
        "success": True,
        "test_success": True,
        "stat": [{
            "test_success": True,
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
        "details": test_results
    }
    for test_result in test_results:
        if test_result["test_success"]:
            summary["stat"][0]["success"] += 1
        else:
            summary["stat"][0]["failed"] += 1
        summary["success"] &= test_result["success"]
        summary["test_success"] &= test_result["test_success"]
        summary["stat"][0]["test_success"] = summary["test_success"]
    return summary
