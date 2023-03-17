import json

from app.utils.dingtalk import DingTalk
from app.curd.facade.http.report import ReportFacade
from app.libs.http_run import HttpRunning


def execute_plan(testcases, config, plan, env_name, create_user, **kwargs):
    http_run = HttpRunning(testcases, config.to_dict())
    summary = http_run.run_testcase()
    report_info = {
        "name": plan.name,
        "test_begin_time": summary["stat"][0]["start_time"],
        "duration": summary["stat"][0]["duration"],
        "create_user": create_user,
        "total": summary["stat"][0]["total"],
        "passed": summary["stat"][0]["success"],
        "failed": summary["stat"][0]["failed"],
        "pass_rate": "{}%".format(round(summary["stat"][0]["success"] / summary["stat"][0]["total"] * 100, 1)),
        "env_name": env_name,
        "project_id": plan.project_id,
        "summary": json.dumps(summary)
    }
    report = ReportFacade.create(report_info)
    ding_talk = DingTalk(plan.webhook)
    ding_talk.send_msg(report_url="http://127.0.0.1:5555/#/http/report/view?report_id={}".format(report.id),
                       **report_info)
