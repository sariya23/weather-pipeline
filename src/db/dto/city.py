from dataclasses import dataclass

from src.models.coordinate import Coordinate


@dataclass
class City:
    id: int
    city: str
    coordinates: Coordinate
