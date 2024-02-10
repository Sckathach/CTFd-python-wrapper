from typing import Dict, Optional, List, Any, Tuple

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

    def setup(self, url: str, token: str, verbose: str = "minimal") -> None:
        """
        Set up the client at the beginning of the script.

        :param url: URL of form https://your-ctfd/api/v1.
        :param token: TOKEN generated from the setting page of an admin account of the CTFd.
        :param verbose: The verbose can be set to "no", "minimal", "simple" or "debug".
        :return: None
        """
        self.http.token = Token.create(token)
        self.http.url = url

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

    def update_challenge(self, challenge: Challenge) -> Challenge:
        data = challenge.to_dict()
        response = self.http.update_challenge(data)
        print(response)
        challenge = Challenge.from_dict(response)
        self.challenges[str(challenge.id)] = challenge
        return challenge

    def add_challenge(self, challenge: Challenge) -> Challenge:
        """
        Upload a challenge to the CTFd.

        :param challenge: Challenge to upload (if the challenge was never uploaded, its id is -1)
        :return: Challenge with updated id.
        """
        response = self.http.create_challenge(challenge.to_dict())
        challenge.id = response["id"]
        self.challenges[str(challenge.id)] = challenge
        return challenge

    def attempt_challenge_with_ctfd_check(
        self, challenge, provided: str, token: Optional[str] = None
    ) -> bool:
        """
        Attempt the challenge with the CTFd verification.

        :param challenge:
        :param provided:
        :param token: (Optional) Can be the token of someone else.
        :raise: HiddenChallengeError if the challenge is hidden.
        """
        if challenge.state == "hidden":
            raise HiddenChallengeError("Impossible to attempt hidden challenge.")
        else:
            result = self.http.attempt_challenge(challenge.id, provided, token=token)[
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
        """
        Attempt the challenge with the wrapper verification.

        :param provided:
        :param challenge_id:
        :param user_id:
        :param team_id: (Optional)
        :return:
        """
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
        """
        List (prints) all local challenges. Be sure to fetch the existing challenges on the CTFd beforehand.

        :return: None
        """
        for _, challenge in self.challenges.items():
            print(challenge)

    def fetch_challenges(self) -> None:
        challenges = self.http.get_challenges()
        for challenge in challenges:
            if str(challenge["id"]) in self.challenges.keys():
                # TODO: make sure it does not create issues
                # get_challenges do not fetch every field, so it is overwritten by the template
                # It might be mandatory to fetch challenges one by one, even those not already in the client
                # they might have been created with the CTFd GUI
                c = Challenge.from_dict(self.http.get_challenge(challenge["id"]))
            else:
                c = Challenge.from_dict(challenge)
            self.challenges[str(challenge["id"])] = c

    def delete_challenge(self, challenge_id: int) -> None:
        """
        Deletes a challenge locally.

        :param challenge_id:
        :return: None
        """
        self.challenges.pop(str(challenge_id))
        self.log.debug(f"Challenge {challenge_id} deleted.")

    def delete_challenges(self) -> None:
        """
        Delete all the challenges of the CTFd.

        :return: None
        """
        for _, challenge in self.challenges.items():
            self.http.delete_challenge(challenge.id)
            self.log.debug(f"Challenge {challenge.id} deleted.")
        self.challenges = {}

    """
        Flags 
    """

    def add_flag(self, flag: Flag) -> Flag:
        """
        Upload a flag to the CTFd.

        :param flag: Flag to upload (if the flag was never uploaded, its id is -1)
        :return: Flag with updated id.
        """
        response = self.http.create_flag(flag.to_dict())
        flag.id = response["id"]
        self.flags[str(flag.id)] = flag
        return flag

    def fetch_challenge_flags(self, challenge_id: int) -> None:
        flags = self.http.get_challenge_flags(challenge_id)
        for flag in flags:
            self.flags[str(flag["id"])] = Flag.from_dict(flag)

    def fetch_flags(self) -> None:
        flags = self.http.get_flags()
        for flag in flags:
            self.flags[str(flag["id"])] = Flag.from_dict(flag)

    def delete_flag(self, flag_id: int) -> None:
        """
        Delete a flag locally.

        :param flag_id:
        :return: None
        """
        self.flags.pop(str(flag_id))
        self.log.debug(f"Flag {flag_id} deleted.")

    def delete_flags(self) -> None:
        """
        Delete all flags of the CTFd.

        :return: None
        """
        for _, flag in self.flags.items():
            self.http.delete_flag(flag.id)
            self.log.debug(f"Flag {flag.id} deleted.")
        self.flags = {}

    """
        Users 
    """

    def add_user(self, user: User) -> User:
        """
        Upload a user to the CTFd.

        :param user: User to upload (if the user was never uploaded, its id is -1)
        :return: User with updated id.
        """
        response = self.http.create_user(user.to_dict())
        user.id = response["id"]
        self.users[str(user.id)] = user
        return user

    def fetch_users(self) -> None:
        users = self.http.get_users()
        for user in users:
            self.users[str(user["id"])] = User.from_dict(user)

    def delete_user(self, user_id: int) -> None:
        """
        Delete user locally

        :param user_id:
        :return: None
        """
        self.users.pop(str(user_id))
        self.log.debug(f"User {user_id} deleted.")

    def delete_users(self) -> None:
        """
        Delete every user on the CTFd.

        :return: None
        """
        for _, user in self.users.items():
            self.http.delete_user(user.id)
            self.log.debug(f"User {user.id} deleted.")
        self.users = {}

    def fetch_user_points(self, user_id: int) -> int:
        solves = self.http.get_user_solves(user_id)
        points = 0
        for solve in solves:
            points += solve["challenge"]["value"]
        return points
