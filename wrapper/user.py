import random
import string

template = {
    "id": -1,
    "name": "bob",
    "email": "bob@bob.bob",
    "password": "password",
    "type": "user",
    "verified": False,
    "hidden": False,
    "banned": False,
    "token": "ctfd_6327657374206c6520746f6b656e207375706572207365637265742021",
}


def generate_random_email(local_length: int = 12, domain_length: int = 7) -> str:
    """
    Generate a random email as two emails can not be equal.

    :param local_length: (optional)
    :param domain_length: (optional)
    :return:
    """
    local_part = "".join(
        random.choices(string.ascii_letters + string.digits, k=local_length)
    )
    domain_part = "".join(random.choices(string.ascii_letters, k=domain_length))
    email = f"{local_part}@{domain_part}.com"
    return email


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
        token: str = template["token"],
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type
        self.verified = verified
        self.hidden = hidden
        self.banned = banned
        self.token = token

    def __str__(self) -> str:
        return (
            f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, type={self.type}, "
            f"verified={self.verified}, hidden={self.hidden}, banned={self.banned})"
        )

    def to_dict(self):
        return self.__dict__

    @classmethod
    def create(
        cls,
        name: str,
        email: str = None,
        password: str = template["password"],
    ) -> "User":
        return User(
            name=name,
            email=email if email else generate_random_email(),
            password=password,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(**cls.filter_dict(data))

    @classmethod
    def filter_dict(cls, data):
        return {
            "id": data["id"],
            "name": data["name"],
            "email": data.get("email", template["email"]),
            "password": data.get("password", template["password"]),
            "type": data.get("type", template["type"]),
            "verified": data.get("verified", template["verified"]),
            "hidden": data.get("hidden", template["hidden"]),
            "banned": data.get("banned", template["banned"]),
        }
