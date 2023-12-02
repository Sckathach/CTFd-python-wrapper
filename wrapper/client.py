from typing import Dict, Optional
# from .type import ChallengeType, LogType, HTTPClientType, UserType, FlagType
from .challenge import Challenge
from .http import HTTPClient
from .logs import Log
from .user import User
from .flag import Flag


class Client:
    def __init__(self):
        self.http: HTTPClient = HTTPClient()
        self.challenges: Optional[Dict[str, Challenge]] = {}
        self.users: Optional[Dict[str, User]] = {}
        self.flags: Optional[Dict[str, Flag]] = {}
        self.log: Log = Log("Client")

    def setup(self, url: str, token: str) -> None:
        self.http.token = token
        self.http.url = url
        self.log.debug(f"self.http.token = {self.http.token}, self.http.url = {self.http.url}")

    def push_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.create_challenge(data)
        challenge.id = response["data"]["id"]
        return challenge

    def update_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        return Challenge.from_dict(response["data"])

    def add_challenge(self, challenge: Challenge) -> None:
        x = self.push_challenge(challenge)
        self.challenges[str(x.id)] = x

    def list_challenges(self) -> None:
        for x in self.challenges:
            print(x)

    def fetch_challenges(self) -> None:
        challenges = self.http.get_challenges()
        for chall in challenges:
            self.challenges[str(chall["id"])] = Challenge.from_dict(chall)
