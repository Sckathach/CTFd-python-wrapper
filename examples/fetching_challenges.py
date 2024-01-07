from wrapper.client import Client
from dotenv import load_dotenv
from time import sleep
from random import randint
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:8000/api/v1"

client = Client()
client.setup(URL, TOKEN, verbose="none")

# Fetch the challenges from the CTFd
client.fetch_challenges()

# Get information about a specific challenge, given its id
print(client.challenges["1"].name)

# List all the challenges
for _, chall in client.challenges.items():
    print(chall)

    # and change the description if the challenge is in the PWN category
    if chall.category == "PWN":
        chall.description = "Hihihi"
        client.update_challenge(chall)

# It works the same for the users and the flags :
client.fetch_users()
client.fetch_flags()

print("\n\n\n")
print("Hacking users' passwords...")
sleep(randint(200, 1000) / 100)
print("Sheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesh !")
for _, user in client.users.items():
    print(user.name + ":" + user.password)

print("\n\n\n")
print("Hacking administrator...")
sleep(randint(200, 1000) / 100)
print("Seeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesh !")
for _, flag in client.flags.items():
    print(client.challenges[str(flag.challenge_id)].name + ":" + flag.content)
