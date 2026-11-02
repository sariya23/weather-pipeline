from dataclasses import dataclass
from datetime import date
from typing import Self
from enum import StrEnum, Enum


class TemperatureUnits(StrEnum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'

class WindSpeedUnits(StrEnum):
    ms = 'ms'
    kmh = 'kmh'

class PrecipitationUnits(StrEnum):
    mm = 'mm'
    inch = 'inch'

class TimeFormat(StrEnum):
    iso8601 = 'iso8601'
    unixtime = 'unixtime'

@dataclass
class GetWeatherRequestDTO:
    latitude: float
    longitude: float
    hourly: list[str] | None = None
    start_date: date | None = None
    end_date: date | None = None
    temperature_unit: TemperatureUnits = TemperatureUnits.celsius
    wind_speed_unit: WindSpeedUnits = WindSpeedUnits.kmh
    precipitation_units: PrecipitationUnits = PrecipitationUnits.mm
    timeformat: TimeFormat = TimeFormat.iso8601
