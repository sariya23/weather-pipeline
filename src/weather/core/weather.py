from typing import Protocol
from httpx import Response
from src.weather.models.code.weather import WeatherList, Weather
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO


class IGetWeather(Protocol):
    source_name: str

    def get_weather(self, params: GetWeatherRequestDTO) -> Response:
        pass

    def response_to_domain(self, response: Response) -> Weather:
        pass



class WeatherCore:
    def __init__(self, weather_api: list[IGetWeather]):
        self.__weather_api = weather_api

    def get_weather(self, params: GetWeatherRequestDTO) -> WeatherList:
        result = WeatherList()
        for api_client in self.__weather_api:
            response = api_client.get_weather(params)
            response.raise_for_status()
            model = api_client.response_to_domain(response)
            model.source = api_client.source_name
            result.append(model)
        return result

