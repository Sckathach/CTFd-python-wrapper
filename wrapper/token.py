from typing import Dict, Any
from logs import Log

template = {
    "user_id": -1,
    "type": "user",
    "expiration": "2040-12-12T00:00:00+00:00",
    "id": -1,
    "created": "2020-12-12T00:00:00+00:00",
    "description": "Placeholder",
    "value": "ctfd_6327657374206c6520746f6b656e207375706572207365637265742021"
}


class Token(dict):
    def __init__(
            self,
            user_id: int = template["user_id"],
            type: str = template["type"],
            expiration: str = template["expiration"],
            id: int = template["id"],
            created: str = template["created"],
            description: str = template["description"],
            value: str = template["value"]
    ):
        super().__init__()
        self.user_id: int = user_id
        self.type: str = type
        self.expiration: str = expiration
        self.id: int = id
        self.created: str = created
        self.description: str = description
        self.value: str = value
        self.log = Log(f"Token{id}")

    def __str__(self, secret_threshold=4):
        l1 = len(self.value)
        l2 = l1 // secret_threshold
        token_show = self.value[:l2] + "*" * (l1 - l2)
        self.log.debug(
            f"Token {token_show}"
        )