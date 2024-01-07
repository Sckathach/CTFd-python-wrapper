from wrapper.client import Client
from wrapper.challenge import Challenge
from wrapper.user import User
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
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

    def teardown_method(self, method):
        self.client.delete_users()
        self.client.delete_challenges()
        del self.client
