from dataclasses import dataclass
from datetime import datetime


@dataclass
class InsertWeatherDTO:
    city_id: int
    temperature: float| None
    wind_speed: float| None
    relative_humidity: float| None
    source_id: int
    measure_timestamp: datetime
    rain: float| None
