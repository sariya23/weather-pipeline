from dataclasses import dataclass


@dataclass
class City:
    id: int
    city: str
    longitude: float
    latitude: float
