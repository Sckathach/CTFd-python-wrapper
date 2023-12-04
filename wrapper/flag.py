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
        challenge_id: int= template["challenge_id"],
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

    def __str__(self):
        # TODO: find a better way to __string__ a flag
        return self.content

    def __eq__(self, other) -> bool:
        if isinstance(other, Flag):
            return (
                self.id == other.id
                # and self.id == other.id
                # and self.challenge == other.challenge
                # and self.type == other.type
                # and self.content == other.content
                # and self.data == other.data
            )
        else:
            raise TypeError(f"Expected type Flag, got {other.__class__}")

    @classmethod
    def create(
        cls,
        content,
        challenge,
    ):
        return Flag(content=content, challenge=challenge)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dict):
        return cls(**cls.filter_dict(dict))

    @classmethod
    def filter_dict(cls, data):
        return {
            "challenge_id": data["challenge_id"],
            "id": data["id"],
            "challenge": data["challenge"],
            "type": data["type"],
            "content": data["content"],
            "data": data["data"],
        }
