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

    def _push_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.create_challenge(data)
        challenge.id = response["data"]["id"]
        return challenge

    def _push_flag(self, flag: Flag) -> Flag:
        data = flag.to_dict()
        response = self.http.create_flag(data)
        flag.id = response["data"]["id"]
        return flag

    def update_challenge(self, challenge: Challenge) -> Challenge:
        # flags = challenge.flags
        # flags_remote = self.fetch_challenge_flags(challenge)
        # print("Flags remote: ")
        # for f in flags_remote:
        #     print(f)
        # print("*********************************")
        # new_flags = []
        # new_flags_remote = []
        # for f in flags:
        #     if f not in flags_remote:
        #         new_flags.append(f)
        #     else:
        #         print(f"{f} is in {flags_remote}")
        # for i in range(len(new_flags)):
        #     f = new_flags.pop()
        #     f.challenge_id = challenge.id
        #     f.challenge = challenge.id
        #     f = self._push_flag(f)
        #     print(f"flag {f} pushed")
        #     new_flags_remote.append(f)
        # challenge.flags = new_flags_remote
        # self.challenges[str(challenge.id)] = challenge
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        return Challenge.from_dict(response["data"])

    def add_challenge(self, challenge: Challenge) -> None:
        c = self._push_challenge(challenge)
        new_flags = []
        if len(c.flags) > 0:
            for flag in c.flags:
                flag.challenge_id = c.id
                flag.challenge = c.id
                f = self._push_flag(flag)
                flag.id = f.id
                new_flags.append(f)
        c.flags = new_flags
        self.challenges[str(c.id)] = c

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
            chall_id = str(chall["id"])
            self.challenges[chall_id] = Challenge.from_dict(chall)
            self.fetch_challenge_flags(self.challenges[chall_id])

    def delete_challenge(self, challenge: Challenge) -> None:
        self.challenges.pop(str(challenge.id))
        self.http.delete_challenge(challenge.id)

    # Users
    def add_user(self, user: User) -> User:
        data = self.http.create_user(user.to_dict())
        self.users[str(user.id)] = user
        return User.from_dict(data)
