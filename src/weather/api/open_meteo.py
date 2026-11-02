import logging
from dataclasses import asdict
from datetime import timedelta

import httpx

from src.models.coordinate import Coordinate
from src.weather.models.domain.weather import Weather, WeatherList, WeatherLocation
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO

logger = logging.getLogger(__name__)


class ApiOpenMeteo:
    source_name = "open-meteo"

    def __init__(self, base_url: str):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def get_weather(self, params: GetWeatherRequestDTO) -> httpx.Response:
        with httpx.Client(base_url=self.base_url) as client:
            params_dict = asdict(params)
            if params.start_date:
                params_dict["start_date"] = params.start_date.strftime("%Y-%m-%d")
            if params.end_date:
                params_dict["end_date"] = params.end_date.strftime("%Y-%m-%d")
            logger.debug(f"params: {params_dict}, url: {self.__base_url}")
            response = client.get(self.base_url, params=params_dict)
            return response

    def response_to_domain(
        self, response: httpx.Response, coordinates: Coordinate
    ) -> WeatherList:
        data = response.json()
        hourly = data.get("hourly")
        if not hourly:
            logger.debug(f"no hourly data")
            return WeatherList([])
        utc_offset_seconds = data.get("utc_offset_seconds", 0)
        location = WeatherLocation(coordinates=coordinates)
        res = WeatherList()

        for timestamp, temperature, wind_speed, humidity, rain in zip(
            hourly["time"],
            hourly["temperature_2m"],
            hourly["wind_speed_10m"],
            hourly["relative_humidity_2m"],
            hourly["rain"],
            strict=True,
        ):
            res.append(
                Weather(
                    timestamp=timestamp + timedelta(seconds=utc_offset_seconds),
                    temperature_cel_2m=temperature,
                    wind_speed_mm_10m=wind_speed,
                    relative_humidity_2m=humidity,
                    location=location,
                    rain_mm=rain,
                )
            )
        return res