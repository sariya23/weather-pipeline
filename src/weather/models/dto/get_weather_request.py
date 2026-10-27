from dataclasses import dataclass
from datetime import date


@dataclass
class GetWeatherRequestDTO:
    latitude: float
    longitude: float
    hourly: list[str]
    start_date: date
    end_date: date
