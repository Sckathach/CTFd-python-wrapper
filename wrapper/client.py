from .http import HTTPClient
from typing import Dict, Optional
from types_.challenge import Challenge as ChallengePayload
from types_.user import User as UserPayload
from types_.flag import Flag as FlagPayload
from types_.http import HTTPClient as HTTPClientPayload
from .challenge import Challenge


class Client:
    def __init__(self):
        self.http: HTTPClientPayload = HTTPClient()
        self.challenges: Optional[Dict[str, ChallengePayload]] = {}
        self.users: Optional[Dict[str, UserPayload]] = {}
        self.flags: Optional[Dict[str, FlagPayload]] = {}

    def setup(self, url: str, token: str) -> None:
        self.http.token = token
        self.http.url = url
        print(f"self.http.token = {self.http.token}, self.http.url = {self.http.url}")

    def push_challenge(self, challenge: ChallengePayload) -> ChallengePayload:
        data = challenge.to_dict()
        response = self.http.create_challenge(data)
        challenge.id = response["data"]["id"]
        return challenge

    def update_challenge(self, challenge: ChallengePayload) -> ChallengePayload:
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        return Challenge.from_dict(response["data"])

    def add_challenge(self, challenge: Challenge) -> None:
        x = self.push_challenge(challenge)
        self.challenges[str(x.id)] = x

    def list_challenges(self):
        for x in self.challenges:
            print(x)
