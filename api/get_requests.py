from api.requests_ import request


def get_challenges(token=None, url=None):
    challenges = request("GET", "/challenges", token=token, url=url)
    return challenges["data"]


def get_challenge(challenge_id=0, token=None, url=None):
    challenge = request("GET", f"/challenges/{challenge_id}", token=token, url=url)
    return challenge["data"]


def get_challenge_flags(challenge_id=0, token=None, url=None):
    flags = request("GET", f"/challenges/{challenge_id}/flags", token=token, url=url)
    return flags["data"]


def delete_challenge(challenge_id=0, token=None, url=None):
    request("DELETE", f"/challenges/{challenge_id}", token=token, url=url)
