from dataclasses import dataclass
from datetime import datetime


@dataclass
class InsertWeatherDTO:
    city_id: int
    temperature: float
    wind_speed: float
    relative_humidity: float
    source_id: int
    measure_timestamp: datetime
