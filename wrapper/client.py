from typing import Dict, Optional, List

from .errors import HiddenChallengeError
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
        self.flags: Optional[List[Flag]] = []
        self.log: Log = Log("Client")

    def setup(self, url: str, token: str) -> None:
        self.http.token = token
        self.http.url = url
        self.log.debug(
            f"self.http.token = {self.http.token}, self.http.url = {self.http.url}"
        )

    def push_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.create_challenge(data)
        challenge.id = response["data"]["id"]
        return challenge

    def push_flag(self, flag: Flag) -> Flag:
        data = flag.to_dict()
        response = self.http.create_flag(data)
        flag.id = response["data"]["id"]
        return flag

    def update_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        return Challenge.from_dict(response["data"])

    def add_challenge(self, challenge: Challenge) -> None:
        c = self.push_challenge(challenge)
        self.challenges[str(c.id)] = c
        if len(c.flags) > 0:
            for flag in c.flags:
                flag.challenge_id = c.id
                flag.challenge = c.id
                f = self.push_flag(flag)
                flag.id = f.id

    def attempt_challenge(self, challenge: Challenge, attempt: str) -> bool:
        if challenge.state == "hidden":
            raise HiddenChallengeError("Impossible to attempt hidden challenge.")
        else:
            result = self.http.attempt_challenge(challenge.id, attempt)
            return result == "correct" or result == "already_solved"

    def fetch_challenge_flags(self, challenge: Challenge) -> List[Flag]:
        flags = self.http.get_challenge_flags(challenge.id)
        for flag in flags:
            challenge.flags.append(Flag.from_dict(flag))
        return challenge.flags

    def list_challenges(self) -> None:
        for _, chall in self.challenges.items():
            print(chall)

    def fetch_challenges(self) -> None:
        challenges = self.http.get_challenges()
        for chall in challenges:
            id = str(chall["id"])
            self.challenges[id] = Challenge.from_dict(chall)
            self.fetch_challenge_flags(self.challenges[id])
