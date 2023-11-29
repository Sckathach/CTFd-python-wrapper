from requests.exceptions import ConnectionError
from api.errors import RequestError
from api import TOKEN, URL
from api.logs import log
import requests as rq
import json


def request(request_type, path, data=None, token=TOKEN, url=URL):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        if request_type == "POST":
            r = rq.post(url + path, json=data, headers=headers)
        elif request_type == "GET":
            r = rq.get(url + path, headers=headers)
        elif request_type == "PATCH":
            r = rq.patch(url + path, json=data, headers=headers)
        elif request_type == "DELETE":
            r = rq.delete(url + path, headers=headers)
        else:
            raise RequestError(f"Unsupported request type: {request_type}")

        if r.status_code != 200:
            raise RequestError(f"{request_type} error with status: {r.status_code}")
        else:
            log("SIMPLE", f"POST {path} SUCCESS")
            log("FULL", f"{json.dumps(data, indent=4)}")
        return r.json()
    except ConnectionError as conn_err:
        log("ANYWAY", f"ERROR: {conn_err}")
        log("ANYWAY", "INFO: Is it connected?")
        raise ConnectionError(f"{conn_err}")
    except Exception as err:
        log("ANYWAY", f"ERROR: {err}, URL: {url}, TOKEN: {token}")
        raise Exception("Request failed")
