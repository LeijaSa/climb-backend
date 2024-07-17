from datetime import datetime
from typing import TypedDict


class BoulderProblemPayload(TypedDict):
    id: int
    description: str
    grade: str
    state: str
    add_date: datetime
    location_id: int


class LocationPayload(TypedDict):
    id: int
    name: str
    location: str
