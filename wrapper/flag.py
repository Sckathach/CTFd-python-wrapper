from typing import Dict, Any

template = {
    "challenge_id": -1,
    "id": -1,
    "challenge": -1,
    "type": "static",
    "content": "password",
    "data": "",
}


class Flag:
    def __init__(
        self,
        challenge_id: int = template["challenge_id"],
        id: int = template["id"],
        challenge: int = template["challenge"],
        type: str = template["type"],
        content: str = template["content"],
        data: str = template["data"],
    ):
        self.challenge_id = challenge_id
        self.id = id
        self.challenge = challenge
        self.type = type
        self.content = content
        self.data = data

    def __str__(self) -> str:
        # TODO: find a better way to __string__ a flag
        return self.content

    def __eq__(self, other: 'Flag') -> bool:
        if isinstance(other, Flag):
            return (
                self.id == other.id
                and self.id == other.id
                and self.challenge == other.challenge
                and self.type == other.type
                and self.content == other.content
                and self.data == other.data
            )
        else:
            raise TypeError(f"Expected type Flag, got {other.__class__}")

    @classmethod
    def create(
        cls,
        content: str,
        challenge: int,
    ) -> 'Flag':
        return Flag(content=content, challenge=challenge)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Flag':
        return cls(**cls.filter_dict(data))

    @classmethod
    def filter_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "challenge_id": data["challenge_id"],
            "id": data["id"],
            "challenge": data["challenge"],
            "type": data["type"],
            "content": data["content"],
            "data": data["data"],
        }
