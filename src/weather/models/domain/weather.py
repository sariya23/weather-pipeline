from collections import UserList
from datetime import datetime

from pydantic import BaseModel

from src.place.models.domain.place import Place


class Weather(BaseModel):
    timestamp: datetime
    temperature_cel_2m: float | None
    wind_speed_mm_10m: float | None
    relative_humidity_2m: float | None
    rain_mm: float | None
    place: Place
    source: str | None = None


class WeatherList(UserList):
    @property
    def sources(self) -> list[str]:
        return list(set(i.source for i in self.data))
