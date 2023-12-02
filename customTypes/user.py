from typing import TypedDict, Optional


class User(TypedDict):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    type: Optional[str]
    verified: Optional[bool]
    hidden: Optional[bool]
    banned: Optional[bool]
