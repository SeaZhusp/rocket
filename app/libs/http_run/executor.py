import asyncio
import json

from app.core.decorator import exception_log
from app.curd.facade.manage.envconfig import EnvConfigFacade
from app.utils.dingtalk import DingTalk
from app.curd.facade.http.report import ReportFacade
from app.libs.http_run import HttpRunning


@exception_log
async def async_execute_plan(testcases, plan, env_name, create_user, **kwargs):
    config_map = await EnvConfigFacade.get_and_parse_config(pk=plan.env_id)
    http_run = HttpRunning(testcases, config_map)
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


# 包装异步函数为同步函数， 线程中执行异步协程方法会报错
def sync_execute_plan(testcases, plan, env_name, create_user, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_execute_plan(testcases, plan, env_name, create_user, **kwargs))
    loop.close()
    return result
