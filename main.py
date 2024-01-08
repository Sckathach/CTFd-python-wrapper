from wrapper.challenge import Challenge
from wrapper.client import Client
from wrapper.user import User
from wrapper.flag import Flag
from dotenv import load_dotenv
from time import sleep
from random import randint
import numpy as np
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = "http://127.0.0.1:8000/api/v1"

client = Client()
client.setup(URL, TOKEN, verbose="simple")

client.fetch_users()
client.fetch_challenges()
client.fetch_flags()
client.delete_users()
client.delete_challenges()

user = User.create("Bob")
user = client.add_user(user)
challenge = Challenge.create("Bof3", "PWN")
challenge = client.add_challenge(challenge)
flag = Flag.create("flag", challenge.id)
flag = client.add_flag(flag)

client.attempt_challenge("fdjkslfmj", challenge.id, user.id)
client.mark_as_solved(challenge.id, user.id)


def pick_random_gaussian(length: int, mean: int, std_dev: int) -> int:
    """
    Picks a random item from the list with a Gaussian distribution.

    :param length:
    :param mean: The mean of the Gaussian distribution.
    :param std_dev: The standard deviation of the Gaussian distribution.
    :return: The chosen index
    """

    # Ensure the mean and standard deviation are within the bounds of the list
    mean = max(0, min(mean, length - 1))
    std_dev = max(1, std_dev)

    # Generate a random index using Gaussian distribution
    index = int(np.random.normal(mean, std_dev))

    # Clamp the index to the bounds of the list
    index = max(0, min(index, length - 1))
    return index

#
# while 1:
#     print("test?")
#     chall = randint(0, 100)
#     user = pick_random_gaussian(100, 50, 10)
#     print(user, chall)
#     client.mark_as_solved(chall, user)
#     sleep(1)
