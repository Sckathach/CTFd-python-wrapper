from wrapper.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:4000/api/v1"

client = Client()
client.setup(URL, TOKEN)

# Fetch the challenges from the CTFd
client.fetch_challenges()

# Get information about a specific challenge, given its id
print(client.challenges["1"].name)

# List all the challenges
for _, chall in client.challenges.items():
    print(chall)
