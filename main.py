import argparse
from datetime import datetime

from src.config import Config

import logging

from src.weather.api.open_meteo import ApiOpenMetio
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO
from src.weather.core.weather import WeatherCore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
                        prog='WeatherPipeline',
                        description='Pipeline for downloading weather data')
    parser.add_argument('config')
    args = parser.parse_args()

    config = Config(_env_file=args.config)
    open_meteo_api = ApiOpenMetio(config.base_url)
    weather = WeatherCore(weather_api=[open_meteo_api])
    return weather.get_weather(GetWeatherRequestDTO.moscow(hourly=[
        'temperature_2m', 'relative_humidity_2m', 'rain,wind_speed_10m'],
        start_date=datetime.today(), end_date=datetime.today()))



if __name__ == '__main__':
    print(main())
