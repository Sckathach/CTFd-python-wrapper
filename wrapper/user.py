template = {
    "id": -1,
    "name": "bob",
    "email": "bob@bob.bob",
    "password": "password",
    "type": "user",
    "verified": False,
    "hidden": False,
    "banned": False,
}


class User:
    def __init__(
        self,
        id: int = template["id"],
        name: str = template["name"],
        email: str = template["email"],
        password: str = template["password"],
        type: str = template["type"],
        verified: bool = template["verified"],
        hidden: bool = template["hidden"],
        banned: bool = template["banned"],
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type
        self.verified = verified
        self.hidden = hidden
        self.banned = banned

    def __str__(self) -> str:
        return (
            f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, type={self.type}, "
            f"verified={self.verified}, hidden={self.hidden}, banned={self.banned})"
        )

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        print(f"Creating user from data: {data}")
        return cls(**cls.filter_dict(data))

    @classmethod
    def create(cls, name):
        id = -1
        email = name + "@sckathach.ai"
        password = name + "pass"
        return User(id, name, email, password)

    @classmethod
    def filter_dict(cls, data):
        return {
            "id": data["id"],
            "name": data["name"],
            "email": data["email"],
            "password": data["password"],
            "type": data["type"],
            "verified": data["verified"],
            "hidden": data["hidden"],
            "banned": data["banned"],
        }
