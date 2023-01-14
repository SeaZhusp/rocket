from fastapi import APIRouter

from ext.apirunner.http_client import HttpClient

router = APIRouter(prefix='/case')


@router.post('/run')
async def run_single():
    url = '1'
    kwargs = {
        "data": {"categoryId": "1514619214747518978"},
        "headers": {
            "content-type": "application/json;charset=UTF-8",
            "source": "501",
            "token": "eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6ImEzMGY0OWVjLWU0YTktNGE2Zi1hNzIxLTUwNTI1MWYwNzJiOSIsInVzZXJJZCI6ImIxZjg3MjFiLTZlNjUtNDA5ZC05ODljLWZkZTNmYTJkMGRiZCIsImNsdXN0ZXJJZCI6ImFsaXByb2QiLCJleHAiOjE2NzQwNTc0NzJ9.wElm5F9oRgQRpCrTDAMUBPexCnWIvVhtLGFZPU_9CqaO5sJSnrA6CUDkLhmJnfvnfWq8h5E3XtBdVcu2PvzHrQ"
        }
    }
    response = HttpClient(url, **kwargs).send_request('post')
    return response
