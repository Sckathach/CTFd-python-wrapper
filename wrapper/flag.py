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

    def __eq__(self, other: "Flag") -> bool:
        # Check if two flags are equals before push, which means it does not look the flag.id which is not properly set
        # yet.
        if isinstance(other, Flag):
            return (
                # self.id == other.id
                self.challenge == other.challenge
                and self.challenge_id == other.challenge_id
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
        challenge_id: int,
    ) -> "Flag":
        return Flag(content=content, challenge=challenge_id, challenge_id=challenge_id)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Flag":
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
