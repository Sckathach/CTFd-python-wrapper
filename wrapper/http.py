from typing import Optional, Dict, List, Any
from .flag import Flag
from .token import Token
import requests as rq
import json

from .errors import RequestError, CTFdAPIError
from .logs import Log


class HTTPClient:
    def __init__(self):
        self.token: Optional[Token] = None
        self.url: Optional[str] = None
        self.log = Log("HTTPClient")

    def request(
            self,
            request_type: str,
            path: str,
            data: Dict[str, Any] = None,
            token: Optional[str] = None,
            request_data: Optional[bool] = True
    ) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {token if token else self.token.value}",
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
                self.log.error(r.json())
                raise RequestError(f"{request_type} error with status: {r.status_code}")
            else:
                rj = r.json()
                if "success" in rj.keys() and rj["success"]:
                    self.log.info(f"{request_type} {path} SUCCESS")
                    self.log.debug(f"{json.dumps(rj, indent=4)}")
                    if request_data and "data" not in rj.keys():
                        raise RequestError("No data in response")
                    elif "data" in rj.keys():
                        return rj["data"]
                    else:
                        return rj
                else:
                    self.log.info(f"{request_type} {path} ERROR")
                    # self.log.error(f"{json.dumps(rj, indent=4)}")
                    raise CTFdAPIError(f"{json.dumps(rj, indent=4)}")
        except ConnectionError as conn_err:
            self.log.error(f"{conn_err}")
            self.log.info("Is it connected?")
            self.log.error("FATAL: EXITING...")
            exit(1)
        except Exception as err:
            self.log.error(f"{err}")
            self.log.debug(f"URL: {self.url}, TOKEN: {self.token}")
            self.log.error("FATAL: EXITING...")
            exit(1)

    """
        Challenges 
    """

    def get_challenges(self) -> Dict[str, Any]:
        return self.request("GET", "/challenges?view=admin")

    def get_challenge(self, challenge_id: int = 0) -> Dict[str, Any]:
        return self.request("GET", f"/challenges/{challenge_id}")

    def get_challenge_flags(self, challenge_id: int = 0) -> Dict[str, Any]:
        return self.request("GET", f"/challenges/{challenge_id}/flags")

    def delete_challenge(self, challenge_id: int = 0) -> Dict[str, Any]:
        return self.request("DELETE", f"/challenges/{challenge_id}", request_data=False)

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

    def attempt_challenge(
            self, challenge_id: int, flag: str, token: Optional[str] = None
    ) -> Dict[str, Any]:
        d = {"challenge_id": challenge_id, "submission": flag}
        return self.request("POST", "/challenges/attempt", data=d, token=token)

    def submission(
            self,
            challenge_id: int,
            user_id: int,
            team_id: Optional[int] = None,
            token: Optional[str] = None,
    ) -> Dict[str, Any]:
        print("bonsoir")
        d = {
            "provided": "MARKED AS SOLVED BY ADMIN",
            "user_id": user_id,
            "team_id": team_id,
            "challenge_id": challenge_id,
            "type": "correct",
        }
        return self.request("POST", "/submissions", data=d, token=token)

    def update_challenge(self, data) -> Dict[str, Any]:
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

    """
        Users 
    """

    def get_users(self) -> Dict[str, Any]:
        return self.request("GET", "/users")

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

    def delete_user(self, user_id: int = 0) -> Dict[str, Any]:
        return self.request("DELETE", f"/users/{user_id}", request_data=False)

    """
        Flags
    """

    def create_flag(self, data) -> Dict[str, Any]:
        d = {
            "content": data["content"],
            "data": data["data"],
            "type": data["type"],
            "challenge": data["challenge"],
        }
        return self.request("POST", "/flags", data=d)

    def get_flags(self) -> Dict[str, Any]:
        return self.request("GET", "/flags")

    def delete_flag(self, flag_id: int = 0) -> Dict[str, Any]:
        return self.request("DELETE", f"/flags/{flag_id}", request_data=False)
