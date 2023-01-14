import json

import requests


class HttpClient(object):
    def __init__(self, url, session=False, timeout=30, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.timeout = timeout
        self.client = requests.session() if session else requests

    # @staticmethod
    # def _get_elapsed(timer: datetime.timedelta):
    #     if timer.seconds > 0:
    #         return f"{timer.seconds}.{timer.microseconds / 1000}s"
    #     return f"{timer.microseconds / 1000}ms"

    def send_request(self, method: str):
        try:
            resp_object = self.client.request(method.upper(), self.url, **self.kwargs)
            status_code = resp_object.status_code
            if status_code >= 400:
                return self.response(False)
            return self.response(True, resp_object)
        except Exception as e:
            return self.response(False, msg=str(e))

    @staticmethod
    def _get_response(response):
        try:
            return response.json()
        except:
            return response.text

    def response(self, result, resp_object=None, msg="success"):
        status_code = -1
        elapsed = "-1ms"
        response = None
        response_headers = None
        data = self.kwargs.get('data')
        request_headers = self.kwargs.get('headers')
        request_data = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
        if resp_object:
            response_headers = resp_object.headers
            request_headers = resp_object.request.headers
            response = self._get_response(resp_object)
            elapsed = resp_object.elapsed
        return {
            "result": result, "response": response, "status_code": status_code, "msg": msg, "elapsed": elapsed,
            "request_data": request_data,
            "response_headers": response_headers, "request_headers": request_headers
        }
