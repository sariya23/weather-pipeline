from collections import UserList
from dataclasses import dataclass


@dataclass
class Place:
    id: int
    city: str
    region: str
    country: str


class PlaceList(UserList):
    def get_place(self, city: str, region: str, country: str) -> Place:
        res, = [i for i in self if i.city == city and i.region == region and i.country == country]
        return res
