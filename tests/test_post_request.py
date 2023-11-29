from api.post_requests import create_user
import random


def test_create_user():
    r = random.randint(1, 1000000)
    data = {
        "name": f"pytest{r}",
        "email": f"pytest{r}@test.com",
        "password": "password",
        "type": "user",
        "verified": False,
        "hidden": True,
        "banned": False,
    }
    assert create_user(data)["success"]
