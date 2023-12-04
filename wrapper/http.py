from typing import Optional, Dict, List, Any
from .flag import Flag
import requests as rq
import json

from .errors import RequestError
from .logs import Log


class HTTPClient:
    def __init__(self):
        self.token: Optional[str] = None
        self.url: Optional[str] = None
        self.log = Log("HTTPClient")

    def request(self, request_type: str, path: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        try:
            if request_type == "POST":
                r = rq.post(self.url + path, json=data, headers=headers)
            elif request_type == "GET":
                r = rq.get(self.url + path, headers=headers)
            elif request_type == "PATCH":
                r = rq.patch(self.url + path, json=data, headers=headers)
            elif request_type == "DELETE":
                r = rq.delete(self.url + path, headers=headers)
            else:
                raise RequestError(f"Unsupported request type: {request_type}")

            if r.status_code != 200:
                raise RequestError(f"{request_type} error with status: {r.status_code}")
            else:
                self.log.info(f"POST {path} SUCCESS")
                self.log.debug(f"{json.dumps(data, indent=4)}")
            return r.json()
        except ConnectionError as conn_err:
            self.log.error(f"{conn_err}")
            self.log.info("Is it connected?")
        except Exception as err:
            self.log.error(f"{err}")
            self.log.debug(f"URL: {self.url}, TOKEN: {self.token}")

    def get_challenges(self) -> Dict[str, Any]:
        challenges = self.request("GET", "/challenges")
        return challenges["data"]

    def get_challenge(self, challenge_id: int = 0) -> Dict[str, Any]:
        challenge = self.request("GET", f"/challenges/{challenge_id}")
        return challenge["data"]

    def get_challenge_flags(self, challenge_id: int = 0) -> List[Dict[str, Any]]:
        flags = self.request("GET", f"/challenges/{challenge_id}/flags")
        return flags["data"]

    def delete_challenge(self, challenge_id: int = 0) -> Dict[str, Any]:
        return self.request("DELETE", f"/challenges/{challenge_id}")

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        d = {
            "name": data["name"],
            "email": data["email"],
            "password": data["password"],
            "type": data["type"],
            "verified": data["verified"],
            "hidden": data["hidden"],
            "banned": data["banned"],
        }
        return self.request("POST", "/users", data=d)

    def create_challenge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        d = {
            "name": data["name"],
            "category": data["category"],
            "description": data["description"],
            "initial": data["initial"],
            "function": data["function"],
            "decay": data["decay"],
            "minimum": data["minimum"],
            "state": data["state"],
            "type": data["type"],
        }
        return self.request("POST", "/challenges", data=d)

    def attempt_challenge(self, challenge_id, flag) -> Dict:
        d = {"challenge_id": challenge_id, "submission": flag}
        return self.request("POST", "/challenges/attempt", data=d)

    def update_challenge(self, data) -> Dict:
        d = {
            "name": data["name"],
            "category": data["category"],
            "description": data["description"],
            "connection_info": data["connection_info"],
            "initial": data["initial"],
            "function": data["function"],
            "decay": data["decay"],
            "minimum": data["minimum"],
            "max_attempts": data["max_attempts"],
            "state": data["state"],
        }
        return self.request("PATCH", f'/challenges/{data["id"]}', data=d)

    def create_flag(self, data) -> Dict:
        d = {
            "content": data["content"],
            "data": data["data"],
            "type": data["type"],
            "challenge": data["challenge"],
        }
        return self.request("POST", "/flags", data=d)
