from collections import UserList
from datetime import datetime

from pydantic import BaseModel


class WeatherLocation(BaseModel):
    longitude: float
    latitude: float
    city_name: str | None = None

class Weather(BaseModel):
    timestamp: datetime
    temperature_cel_2m: float
    wind_speed_10m: float
    relative_humidity_2m: float
    location: WeatherLocation
    source: str | None = None

class WeatherList(UserList):
    pass