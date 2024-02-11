from wrapper.client import Client
from wrapper.challenge import Challenge
from wrapper.user import User
from wrapper.flag import Flag
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:8000/api/v1"


def test_load_token():
    assert TOKEN is not None


class TestClient:
    def setup_method(self, method):
        self.client = Client()
        self.client.setup(URL, TOKEN, verbose="debug")
        self.client.fetch_users()
        self.client.fetch_challenges()
        self.client.fetch_flags()

    def test_create_challenge(self):
        challenge = Challenge.create("Bof 1er", "PWN")
        challenge = self.client.add_challenge(challenge)
        assert challenge.id != -1

    def test_create_user(self):
        user = User.create("Bob 1er")
        user = self.client.add_user(user)
        assert user.id != -1

    def test_create_flag(self):
        challenge = Challenge.create("Bof", "PWN")
        challenge = self.client.add_challenge(challenge)
        assert challenge.id != -1
        flag = Flag.create("flag", challenge.id)
        flag = self.client.add_flag(flag)
        assert flag.id != -1

    def test_flag_check(self):
        flag = Flag.create("flag", 0)
        assert flag.check("flag")
        assert not flag.check("wrong_flag")

    def test_flag_case_insensitive(self):
        flag = Flag(challenge_id=1, data="case_insensitive", content="fLaG")
        assert flag.check("flag")
        assert flag.check("FLAG")

    def test_flag_ctfd(self):
        user = User.create("Bob 2e")
        user = self.client.add_user(user)
        assert user.id != -1
        challenge = Challenge.create("Bof2", "PWN")
        challenge = self.client.add_challenge(challenge)
        assert challenge.id != -1
        flag = Flag.create("flag", challenge.id)
        flag = self.client.add_flag(flag)
        assert flag.id != -1

        assert not self.client.attempt_challenge("wrong_flag", challenge.id, user.id)
        assert self.client.attempt_challenge("flag", challenge.id, user.id)
        assert self.client.get_user_points(user.id) == challenge.value

    def test_marked_as_solved(self):
        user = User.create("Bob 3e")
        user = self.client.add_user(user)
        assert user.id != -1
        challenge = Challenge.create("Bof3", "PWN")
        challenge = self.client.add_challenge(challenge)
        assert challenge.id != -1
        # ! There need to be at least one flag to mark the challenge as solved !
        flag = Flag.create("flag", challenge.id)
        flag = self.client.add_flag(flag)
        assert flag.id != -1

        self.client.mark_as_solved(challenge.id, user.id)
        assert self.client.get_user_points(user.id) == challenge.value

    def test_update_challenge(self):
        challenge = Challenge.create("Bof4", "PWN")
        challenge = self.client.add_challenge(challenge)
        assert challenge.id != -1
        challenge.description = "*Hello there !*"
        challenge = self.client.update_challenge(challenge)
        assert challenge.description == "*Hello there !*"

        self.client.fetch_challenges()
        assert (
            self.client.challenges[str(challenge.id)].description == "*Hello there !*"
        )

    def teardown_method(self, method):
        self.client.delete_users()
        self.client.delete_challenges()
        del self.client
