from typing import Dict, Any

template = {
    "id": -1,
    "date": "1111-11-11T11:11:11.111111+00:00",
    "challenge_id": -1,
    "user_id": -1,
    "ip": "?",
    "type": "correct",
    "provided": "Placeholder",
}


class Submission(dict):
    def __init__(
        self,
        id: int = template["id"],
        date: str = template["date"],
        challenge_id: int = template["challenge_id"],
        user_id: int = template["user_id"],
        ip: str = template["ip"],
        type: str = template["type"],
        provided: str = template["provided"],
    ):
        super().__init__()
        self.id = id
        self.date = date
        self.challenge_id = challenge_id
        self.user_id = user_id
        self.ip = ip
        self.type = type
        self.provided = provided

    def __str__(self) -> str:
        return (
            f"Solve(id={self.id}, date={self.date}, challenge_id={self.challenge_id} "
            f"provided={self.provided}"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Submission":
        return cls(**cls.filter_dict(data))

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def filter_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = template["user_id"]
        if "user_id" in data.keys():
            user_id = data["user_id"]
        elif "user" in data.keys() and "id" in data["user"].keys():
            user_id = data["user"]["id"]
        return {
            "id": data.get("id"),
            "date": data.get("date", template["date"]),
            "challenge_id": data.get("challenge_id", template["challenge_id"]),
            "user_id": user_id,
            "ip": data.get("ip", template["ip"]),
            "type": data.get("type", template["type"]),
            "provided": data.get("provided", template["provided"]),
        }
