from typing import Optional, TypedDict, List
from .flag import Flag


class Challenge(TypedDict):
    id: Optional[int]
    name: Optional[str]
    category: Optional[str]
    description: Optional[str]
    initial: Optional[int]
    value: Optional[int]
    minimum: Optional[int]
    function: Optional[str]
    decay: Optional[int]
    type: Optional[str]
    state: Optional[str]
    solves: Optional[int]
    connection_info: Optional[str]
    tags: Optional[List[str]]
    max_attempts: Optional[int]
    solved_by_me: Optional[bool]
    flags: Optional[List[Flag]]
