from httprunner.utils import get_platform


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
        "details": test_results
    }
    duration = 0
    for test_result in test_results:
        if test_result["success"]:
            summary["stat"][0]["success"] += 1
        else:
            summary["stat"][0]["failed"] += 1

        duration += test_result["time"]["duration"]

        summary["success"] &= test_result["success"]
    summary["stat"][0]["duration"] = round(duration, 2)
    return summary
