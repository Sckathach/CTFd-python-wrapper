from typing import TypedDict, Optional


class Flag(TypedDict):
    challenge_id: Optional[int]
    id: Optional[int]
    challenge: Optional[int]
    type: Optional[str]
    content: Optional[str]
    data: Optional[str]
