from wrapper.client import Client
from dotenv import load_dotenv
from wrapper.challenge import Challenge
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

x = Client()
x.setup(URL, TOKEN)

y = Challenge.create("bob", "test")
x.add_challenge(y)
