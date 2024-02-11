from wrapper.challenge import Challenge
from wrapper.client import Client
from wrapper.user import User
from wrapper.flag import Flag
from time import sleep
from random import randint
import numpy as np

template = {
    "category": "PWN",
    "user": "Bob",
    "challenge": "Bof",
    "flag": "flag"
}


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
    index = max(1, min(index, length - 1))
    return index


class Simulation(Client):
    def __init__(self, token, url, verbose="simple"):
        super().__init__()
        self.setup(url, token, verbose)
        self.fetch_users()
        self.fetch_challenges()
        self.fetch_flags()

    def clean(self) -> None:
        self.delete_users()
        self.delete_challenges()

    def get_nb_users(self) -> int:
        return max([int(x) for x in list(self.users.keys())])

    def get_nb_challenges(self) -> int:
        return max([int(x) for x in list(self.challenges.keys())])

    def create_players(self, nb_players=100) -> None:
        # self.fetch_users(), should be useless
        start = self.get_nb_users()
        for i in range(start, start + nb_players):
            user = User.create(template["user"] + str(i))
            user = self.add_user(user)

    def create_challenges(self, nb_challenges=100) -> None:
        start = self.get_nb_challenges()
        for i in range(start, start + nb_challenges):
            challenge = Challenge.create(template["challenge"] + str(i), template["category"])
            challenge = self.add_challenge(challenge)
            flag = Flag.create(template["flag"], challenge.id)
            flag = self.add_flag(flag)

    def run_simple_gaussian_uniform(self, interval=1, ticks=np.inf, mean=None, std_dev=None):
        i = 0
        nb_challenges = self.get_nb_challenges()
        nb_users = self.get_nb_users()
        if mean is None:
            mean = int(nb_users / 2)
        if std_dev is None:
            std_dev = int(nb_users / 4)
        while i < ticks:
            chall = randint(0, nb_challenges - 1)
            user = pick_random_gaussian(nb_users, mean, std_dev)
            print(f"TIME: {i}, USER: {user}, CHALLENGE: {chall}")
            self.mark_as_solved(chall, user)
            sleep(interval)
