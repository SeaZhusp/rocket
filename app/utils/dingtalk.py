import requests


class DingTalk(object):

    def __init__(self, url: str):
        self.url = url

    def send_msg(self, name, total, passed, failed, pass_rate, report_url, **kwargs):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试结果",
                "text": f"#### 【{name}】 \n\n "
                        f">用例总数：{total}\n\n "
                        f">通过数：{passed} \n\n "
                        f">失败数：{failed} \n\n "
                        f">通过率：{pass_rate} \n\n "
                        "--- \n\n "
                        f">2023-01-01 17:00:00 发布 [查看详情]({report_url}) \n\n "
                        "@朱胜平"
            }
        }
        headers = {
            "content-type": "application/json"
        }
        r = requests.post(self.url, json=data, headers=headers, verify=False)
        if r.json().get("errcode") != 0:
            raise Exception("发送钉钉通知失败")
