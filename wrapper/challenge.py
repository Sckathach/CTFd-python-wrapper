from .flag import Flag
from typing import List, Dict, Any

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


class Challenge:
    def __init__(
        self,
        id: int = template["id"],
        name: str = template["name"],
        category: str = template["category"],
        description: str = template["description"],
        initial: int = template["initial"],
        value: int = template["value"],
        minimum: int = template["minimum"],
        function: str = template["function"],
        decay: int = template["decay"],
        type: str = template["type"],
        state: str = template["state"],
        solves: int = template["solves"],
        connection_info: str = template["connection_info"],
        tags: List[str] = template["tags"],
        max_attempts: int = template["max_attempts"],
        solved_by_me: bool = template["solved_by_me"],
        flags: List[Flag] = template["flags"],
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

    def __str__(self) -> str:
        # TODO: find a better way to __string__ a challenge
        return self.name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Challenge':
        return cls(**cls.filter_dict(data))

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def create(
        cls,
        name: str,
        category: str,
        description: str = template["description"],
        initial: int = template["initial"],
    ) -> 'Challenge':
        return Challenge(
            name=name, category=category, description=description, initial=initial
        )

    @classmethod
    def filter_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # TODO: fix the overwrites, for example, "function" is not present in the respone of the GET request so it
        #  will overwrite the function value of the challenge to ""
        return {
            "id": data["id"],
            "type": data.get("type", template["type"]),
            "name": data.get("name", template["name"]),
            "value": data.get("value", template["value"]),
            "solves": data.get("solves", template["solves"]),
            "category": data.get("category", template["category"]),
            "description": data.get("description", template["description"]),
            "initial": data.get("initial", template["initial"]),
            "decay": data.get("decay", template["decay"]),
            "minimum": data.get("minimum", template["minimum"]),
            "connection_info": data.get("connection_info", template["connection_info"]),
            "tags": data.get("tags", template["tags"]),
            "state": data.get("state", template["state"]),
            "function": data.get("function", template["function"]),
            "max_attempts": data.get("max_attempts", template["max_attempts"]),
            "solved_by_me": data.get("solved_by_me", template["solved_by_me"]),
        }

    def add_flag(self, flag: Flag) -> None:
        flag.challenge = self.id
        flag.challenge_id = self.id
        if flag not in self.flags:
            self.flags.append(flag)
        self.flags.append(flag)
