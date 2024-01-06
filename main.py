from wrapper.client import Client
from wrapper.flag import Flag
from wrapper.challenge import Challenge
from wrapper.user import User
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:8000/api/v1"

client = Client()
client.setup(URL, TOKEN, verbose="debug")

client.fetch_challenges()

for _, chall in client.challenges.items():
    chall.description = "*Placeholder...*"
    client.update_challenge(chall)
