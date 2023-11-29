import json


def pretty(data):
    return json.dumps(data, indent=4, sort_keys=False)
