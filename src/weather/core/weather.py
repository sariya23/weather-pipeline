from typing import Protocol

from httpx import Response

from src.models.coordinate import Coordinate
from src.weather.models.domain.weather import WeatherList
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO


class IGetWeather(Protocol):
    source_name: str

    def get_weather(self, params: GetWeatherRequestDTO) -> Response:
        pass

    def response_to_domain(
        self, response: Response, coordinates: Coordinate
    ) -> WeatherList:
        pass


class WeatherCore:
    def __init__(self, weather_api: IGetWeather):
        self.__weather_api = weather_api

    def get_weather(self, params: GetWeatherRequestDTO) -> WeatherList:
        result = WeatherList()
        response = self.__weather_api.get_weather(params)
        response.raise_for_status()
        models = self.__weather_api.response_to_domain(
            response,
            Coordinate(latitude=params.latitude, longitude=params.longitude),
        )
        for model in models:
            model.source = self.__weather_api.source_name
        result.extend(models)
        return result
