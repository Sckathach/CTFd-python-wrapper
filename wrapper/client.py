from typing import Dict, Optional, List

from .errors import HiddenChallengeError
from .challenge import Challenge
from .http import HTTPClient
from .logs import Log
from .user import User
from .flag import Flag
from .token import Token


class Client:
    def __init__(self):
        self.http: HTTPClient = HTTPClient()
        self.challenges: Optional[Dict[str, Challenge]] = {}
        self.users: Optional[Dict[str, User]] = {}
        self.flags: Optional[Dict[str, Flag]] = {}
        self.log: Log = Log("Client")

    def setup(
        self, url: str, token: str, verbose: str = "minimal"
    ) -> None:
        self.http.token = Token.create(token)
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
        self.log.debug(
            f"self.http.token = {self.http.token}, self.http.url = {self.http.url}"
        )

    """
        Challenges 
    """

    def _push_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.create_challenge(data)
        challenge.id = response["id"]
        return challenge

    def update_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        return Challenge.from_dict(response)

    def add_challenge(self, challenge: Challenge) -> Challenge:
        c = self._push_challenge(challenge)
        self.challenges[str(c.id)] = c
        return c

    def attempt_challenge_with_ctfd_check(
        self, challenge: Challenge, attempt: str, token: Optional[str] = None
    ) -> bool:
        if challenge.state == "hidden":
            raise HiddenChallengeError("Impossible to attempt hidden challenge.")
        else:
            result = self.http.attempt_challenge(challenge.id, attempt, token=token)[
                "status"
            ]
            return result == "correct" or result == "already_solved"

    def attempt_challenge(
        self,
        provided: str,
        challenge_id: int,
        user_id: int,
        team_id: Optional[int] = None,
    ) -> bool:
        for _, flag in self.flags.items():
            if flag.challenge_id == challenge_id or flag.challenge == challenge_id:
                if flag.check(provided):
                    self.http.submission(challenge_id, user_id, team_id)
                    return True
        return False

    def mark_as_solved(
            self,
            challenge_id: int,
            user_id: int,
            team_id: Optional[int] = None,
    ) -> None:
        for _, flag in self.flags.items():
            if flag.challenge_id == challenge_id or flag.challenge == challenge_id:
                self.http.submission(challenge_id, user_id, team_id)

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
        flag.id = response["id"]
        return flag

    def add_flag(self, flag: Flag) -> Flag:
        f = self._push_flag(flag)
        self.flags[str(f.id)] = f
        return f

    def fetch_challenge_flags(self, challenge_id: int) -> None:
        flags = self.http.get_challenge_flags(challenge_id)
        for flag in flags:
            self.flags[str(flag["id"])] = Flag.from_dict(flag)

    def fetch_flags(self) -> None:
        flags = self.http.get_flags()
        for flag in flags:
            self.flags[str(flag["id"])] = Flag.from_dict(flag)

    def delete_flag(self, flag_id: int) -> None:
        self.flags.pop(str(flag_id))
        self.log.debug(f"Flag {flag_id} deleted.")

    def delete_flags(self) -> None:
        for _, flag in self.flags.items():
            self.http.delete_flag(flag.id)
            self.log.debug(f"Flag {flag.id} deleted.")
        self.flags = {}

    """
        Users 
    """

    def add_user(self, user: User) -> User:
        data = self.http.create_user(user.to_dict())
        self.users[str(user.id)] = user
        return User.from_dict(data)

    def fetch_users(self) -> None:
        users = self.http.get_users()
        for user in users:
            self.users[str(user["id"])] = User.from_dict(user)

    def delete_user(self, user_id: int) -> None:
        self.users.pop(str(user_id))
        self.log.debug(f"User {user_id} deleted.")

    def delete_users(self) -> None:
        for _, user in self.users.items():
            self.http.delete_user(user.id)
            self.log.debug(f"User {user.id} deleted.")
        self.users = {}
