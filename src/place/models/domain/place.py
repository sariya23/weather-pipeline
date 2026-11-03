from collections import UserList
from dataclasses import dataclass


@dataclass
class Place:
    id: int
    city: str
    region: str
    country: str


class PlaceList(UserList):
    pass
