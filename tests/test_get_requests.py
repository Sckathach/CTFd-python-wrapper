from api.requests_ import request


def test_simple():
    r = request("GET", "/challenges/1")
    assert r["success"]
