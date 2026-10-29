import httpx
from dataclasses import asdict
import logging

from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO
logger = logging.getLogger(__name__)

class ApiOpenMetio:
    def __init__(self, base_url: str):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def source_name(self) -> str:
        return 'open_metio'

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