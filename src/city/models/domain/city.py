from dataclasses import dataclass

from src.models.coordinate import Coordinate
from collections import UserList

@dataclass
class City:
    id: int
    city: str
    coordinates: Coordinate


class CityList(UserList):
    def get_by_coordinates(self, coordinates: Coordinate) -> City:
        res, = [i for i in self if i.coordinates == coordinates]
        return res