from wrapper.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

client = Client()
client.setup(URL, TOKEN, verbose="debug")

# Fetching the flags (users and challenges are not required)
client.fetch_flags()

# Make the user 3 attempt the challenge 67 with the try "flag", it returns a boolean
print(client.attempt_challenge("flag", 67, 3))
