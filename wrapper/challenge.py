from api.get_requests import get_challenge, get_challenge_flags
from api.post_requests import create_challenge, attempt_challenge, update_challenge
from wrapper.errors import HiddenChallengeError
from wrapper.flag import Flag
from api.logs import log

TOKEN = None
URL = None

template = {
    "id": -1,
    "name": "Placeholder",
    "category": "Placeholder",
    "description": "Placeholder",
    "initial": 1000,
    "value": 1000,
    "minimum": 100,
    "function": "logarithmic",
    "decay": 20,
    "type": "dynamic",
    "state": "visible",
    "solves": 0,
    "connection_info": " ",  # Is recognized as None when I use ""...
    "tags": [],
    "max_attempts": 0,
    "solved_by_me": False,
    "flags": [],
}


def setup(token, url):
    global TOKEN
    global URL
    TOKEN = token
    URL = url


class Challenge:
    def __init__(
        self,
        id=template["id"],
        name=template["name"],
        category=template["category"],
        description=template["description"],
        initial=template["initial"],
        value=template["value"],
        minimum=template["minimum"],
        function=template["function"],
        decay=template["decay"],
        type=template["type"],
        state=template["state"],
        solves=template["solves"],
        connection_info=template["connection_info"],
        tags=template["tags"],
        max_attempts=template["max_attempts"],
        solved_by_me=template["solved_by_me"],
        flags=template["flags"],
    ):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.initial = initial
        self.value = value
        self.minimum = minimum
        self.function = function
        self.decay = decay
        self.type = type
        self.state = state
        self.solves = solves
        self.connection_info = connection_info
        self.tags = tags
        self.max_attempts = max_attempts
        self.solved_by_me = solved_by_me
        self.flags = flags

    def __str__(self):
        # TODO: find a better way to __string__ a challenge
        return self.name

    @classmethod
    def from_dict(cls, dict):
        return cls(**cls.filter_dict(dict))

    def to_dict(self):
        return self.__dict__

    @classmethod
    def create(
        cls,
        name,
        category,
        description=template["description"],
        initial=template["initial"],
    ):
        return Challenge(
            name=name, category=category, description=description, initial=initial
        )

    @classmethod
    def get(cls, challenge_id):
        return cls.from_dict(get_challenge(challenge_id, token=TOKEN, url=URL))

    def push(self):
        data = self.to_dict()
        log("SIMPLE", f"The challenge {self.name} will be pushed.")
        log("FULL", f"{data}")
        response = create_challenge(data, token=TOKEN, url=URL)
        self.id = response["data"]["id"]
        return response

    def update(self):
        data = self.to_dict()
        log("SIMPLE", f"The challenge {self.name}, will be updated.")
        log("FULL", f"{data}")
        response = update_challenge(data, token=TOKEN, url=URL)
        return response

    @classmethod
    def filter_dict(cls, data):
        # TODO: fix the overwrites, for example, "function" is not present in the respone of the GET request so it
        #  will overwrite the function value of the challenge to ""
        return {
            "id": data["id"],
            "type": data["type"],
            "name": data["name"],
            "value": data["value"] if "value" in data.keys() else template["value"],
            "solves": data["solves"],
            "category": data["category"],
            "description": data["description"]
            if "description" in data.keys()
            else template["description"],
            "initial": data["initial"],
            "decay": data["decay"],
            "minimum": data["minimum"],
            "connection_info": data["connection_info"]
            if "connection_info" in data.keys()
            else template["connection_info"],
            "tags": data["tags"] if "tags" in data.keys() else template["tags"],
            "state": data["state"],
            "function": data["function"]
            if "function" in data.keys()
            else template["function"],
            "max_attempts": data["max_attempts"]
            if "max_attempts" in data.keys()
            else template["max_attempts"],
            "solved_by_me": data["solved_by_me"]
            if "solved_by_me" in data.keys()
            else template["solved_by_me"],
        }

    def add_flag(self, content, flag_type="static", data=""):
        flag = Flag(
            challenge_id=self.id,
            challenge=self.id,
            content=content,
            type=flag_type,
            data=data,
        )
        return flag.push(url=URL, token=TOKEN)

    def attempt(self, flag):
        if self.state == "hidden":
            raise HiddenChallengeError("Impossible to attempt hidden challenge.")
        else:
            result = attempt_challenge(self.id, flag, token=TOKEN, url=URL)["data"]["status"]
            return result == "correct" or result == "already_solved"

    def get_flags(self):
        flags = get_challenge_flags(self.id, token=TOKEN, url=URL)
        self.flags = []
        for f in flags:
            self.flags.append(Flag.from_dict(f))

    def get_flag(self):
        flags = get_challenge_flags(self.id, token=TOKEN, url=URL)
        if len(flags) > 0:
            return flags[0]["content"]
        else:
            return ""
