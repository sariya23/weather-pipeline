from dataclasses import dataclass
from typing import Protocol

import httpx

from src.source.models.domain.source import Source
from src.city.models.domain.city import City
from src.models.coordinate import Coordinate
from src.weather.models.domain.weather import WeatherList
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO
from src.weather.models.dto.insert_weather import InsertWeatherDTO


class IWeatherQueries(Protocol):
    def insert_weathers(self, weathers: list[InsertWeatherDTO]):
        pass


class ICityQueries(Protocol):
    def get_city_by_coordinates(self, coordinates: Coordinate) -> City:
        pass

class ISourceQueries(Protocol):
    def get_source_by_name(self, name: str) -> Source:
        pass

class IOpenMeteoApi(Protocol):
    def get_weather(self, params: GetWeatherRequestDTO) -> httpx.Response:
        pass

    def response_to_domain(
        self, response: httpx.Response, coordinates: Coordinate
    ) -> WeatherList:
        pass

class IWeatherCore(Protocol):
    def get_weather(self, params: GetWeatherRequestDTO) -> WeatherList:
        pass


@dataclass
class Database:
    weather: IWeatherQueries
    city: ICityQueries
    source: ISourceQueries

@dataclass
class Core:
    weather: IWeatherCore

@dataclass
class App:
    db: Database
    core: Core