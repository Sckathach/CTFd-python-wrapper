
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
        challenge_id=template["challenge_id"],
        id=template["id"],
        challenge=template["challenge"],
        type=template["type"],
        content=template["content"],
        data=template["data"],
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
