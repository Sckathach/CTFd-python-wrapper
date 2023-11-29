from api.requests_ import request


def create_user(data, token=None, url=None):
    d = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "type": data["type"],
        "verified": data["verified"],
        "hidden": data["hidden"],
        "banned": data["banned"],
    }
    return request("POST", "/users", data=d, token=token, url=url)


def create_challenge(data, token=None, url=None):
    d = {
        "name": data["name"],
        "category": data["category"],
        "description": data["description"],
        "initial": data["initial"],
        "function": data["function"],
        "decay": data["decay"],
        "minimum": data["minimum"],
        "state": data["state"],
        "type": data["type"],
    }
    return request("POST", "/challenges", data=d, token=token, url=url)


def attempt_challenge(challenge_id, flag, token=None, url=None):
    d = {"challenge_id": challenge_id, "submission": flag}
    return request("POST", "/challenges/attempt", data=d, token=token, url=url)


def update_challenge(data, token=None, url=None):
    d = {
        "name": data["name"],
        "category": data["category"],
        "description": data["description"],
        "connection_info": data["connection_info"],
        "initial": data["initial"],
        "function": data["function"],
        "decay": data["decay"],
        "minimum": data["minimum"],
        "max_attempts": data["max_attempts"],
        "state": data["state"],
    }
    return request("PATCH", f'/challenges/{data["id"]}', d, token=token, url=url)


def create_flag(data, token=None, url=None):
    d = {
        "content": data["content"],
        "data": data["data"],
        "type": data["type"],
        "challenge": data["challenge"],
    }
    return request("POST", "/flags", data=d, token=token, url=url)
