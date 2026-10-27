from dataclasses import dataclass
from datetime import date


@dataclass
class GetWeatherRequestDTO:
    latitude: float
    longitude: float
    hourly: list[str] | None = None
    start_date: date | None = None
    end_date: date | None = None
