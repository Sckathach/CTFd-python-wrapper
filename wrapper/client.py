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
        self.flags: Optional[Dict[str, Flag]] = {}
        self.log: Log = Log("Client")

    def setup(
        self, url: str, token: str, verbose: str = "minimal", secret_threshold: int = 4
    ) -> None:
        self.http.token = token
        self.http.url = url

        # Verbose
        if verbose == "no":
            self.log.level = 0
            self.http.log.level = 0
        elif verbose == "minimal":
            self.log.level = 1
            self.http.log.level = 1
        elif verbose == "simple":
            self.log.level = 2
            self.http.log.level = 2
        elif verbose == "debug":
            self.log.level = 3
            self.http.log.level = 3

        # Logs
        l1 = len(self.http.token)
        l2 = l1 // secret_threshold
        token_show = self.http.token[:l2] + "*" * (l1 - l2)
        self.log.debug(
            f"self.http.token = {token_show}, self.http.url = {self.http.url}"
        )

    """
        Challenges 
    """

    def _push_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.create_challenge(data)
        challenge.id = response["data"]["id"]
        return challenge

    def update_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        return Challenge.from_dict(response["data"])

    def add_challenge(self, challenge: Challenge) -> Challenge:
        c = self._push_challenge(challenge)
        self.challenges[str(c.id)] = c
        return c

    def attempt_challenge(self, challenge: Challenge, attempt: str) -> bool:
        if challenge.state == "hidden":
            raise HiddenChallengeError("Impossible to attempt hidden challenge.")
        else:
            result = self.http.attempt_challenge(challenge.id, attempt)["status"]
            return result == "correct" or result == "already_solved"

    def list_challenges(self) -> None:
        for _, chall in self.challenges.items():
            print(chall)

    def fetch_challenges(self) -> None:
        challenges = self.http.get_challenges()
        for chall in challenges:
            self.challenges[str(chall["id"])] = Challenge.from_dict(chall)

    def delete_challenge(self, challenge_id: int) -> None:
        self.challenges.pop(str(challenge_id))
        self.log.debug(f"Challenge {challenge_id} deleted.")

    def delete_challenges(self) -> None:
        for _, chall in self.challenges.items():
            self.http.delete_challenge(chall.id)
            self.log.debug(f"Challenge {chall.id} deleted.")
        self.challenges = {}

    """
        Flags 
    """

    def _push_flag(self, flag: Flag) -> Flag:
        data = flag.to_dict()
        response = self.http.create_flag(data)
        flag.id = response["data"]["id"]
        return flag

    def add_flag(self, flag: Flag) -> Flag:
        f = self._push_flag(flag)
        self.flags[str(f.id)] = f
        return f

    def fetch_challenge_flags(self, challenge_id: int) -> None:
        flags = self.http.get_challenge_flags(challenge_id)
        for flag in flags:
            self.flags[str(flag["id"])] = Flag.from_dict(flag)

    """
        Users 
    """

    def add_user(self, user: User) -> User:
        data = self.http.create_user(user.to_dict())
        self.users[str(user.id)] = user
        return User.from_dict(data)
