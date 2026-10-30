import logging
from dataclasses import asdict

import httpx

from src.weather.models.code.weather import Weather, WeatherList, WeatherLocation
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO

logger = logging.getLogger(__name__)

class ApiOpenMetio:
    source_name = 'open_metio'

    def __init__(self, base_url: str):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def get_weather(self, params: GetWeatherRequestDTO) -> httpx.Response:
        with httpx.Client(base_url=self.base_url) as client:
            params_dict = asdict(params)
            if params.start_date:
                params_dict['start_date'] = params.start_date.strftime('%Y-%m-%d')
            if params.end_date:
                params_dict['end_date'] = params.end_date.strftime('%Y-%m-%d')
            logger.info(f'params: {params_dict}, url: {self.__base_url}')
            response = client.get(self.base_url, params=params_dict)
            return response

    def response_to_domain(self, response: httpx.Response) -> WeatherList:
        data = response.json()
        hourly = data['hourly']
        location = WeatherLocation(
            longitude=data['longitude'],
            latitude=data['latitude'],
        )
        return WeatherList(
            Weather(
                timestamp=timestamp,
                temperature_cel_2m=temperature,
                wind_speed_10m=wind_speed,
                relative_humidity_2m=humidity,
                location=location,
            )
            for timestamp, temperature, wind_speed, humidity in zip(
                hourly['time'],
                hourly['temperature_2m'],
                hourly['wind_speed_10m'],
                hourly['relative_humidity_2m'],
                strict=True,
            )
        )
