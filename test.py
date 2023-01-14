import json

from app.libs.http_client import HttpClient
from app.core.TokenAuth import UserToken


def run_single():
    url = 'http://www.baidu.com'
    kwargs = {
        # "data": {"categoryId": "1514619214747518978"},
        "headers": {
            "content-type": "application/json;charset=UTF-8",
            "source": "501",
            "token": "eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6ImEzMGY0OWVjLWU0YTktNGE2Zi1hNzIxLTUwNTI1MWYwNzJiOSIsInVzZXJJZCI6ImIxZjg3MjFiLTZlNjUtNDA5ZC05ODljLWZkZTNmYTJkMGRiZCIsImNsdXN0ZXJJZCI6ImFsaXByb2QiLCJleHAiOjE2NzQwNTc0NzJ9.wElm5F9oRgQRpCrTDAMUBPexCnWIvVhtLGFZPU_9CqaO5sJSnrA6CUDkLhmJnfvnfWq8h5E3XtBdVcu2PvzHrQ"
        }
    }
    response = HttpClient(url, **kwargs).send_request('get')
    return response


def test_token():
    token = UserToken.generate_token({"id": 1})
    print(token)
    data = UserToken.parse_token(token)
    print(data)


test_token()
