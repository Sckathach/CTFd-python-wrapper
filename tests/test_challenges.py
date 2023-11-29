from wrapper.challenge import Challenge
import random
import pytest


class TestChallenges:
    def setup_method(self, method):
        print(f"Setting up {method}")
        r = random.randint(1, 1000000000)
        self.challenge = Challenge(name=f"pytest{r}", category="Test")
        self.challenge.push()
        self.challenge.add_flag("flag")

    def teardown_method(self, method):
        print(f"Tearing down {method}")
        del self.challenge

    def test_attempt_fail(self):
        assert not self.challenge.attempt("wrong flag")

    def test_attempt_succeed(self):
        assert self.challenge.attempt("flag")
