import argparse
from src.config import Config

import logging

from src.weather.api.open_meteo import ApiOpenMetio
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO

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
    weather_api = ApiOpenMetio(config.base_url)
    return weather_api.get_weather(GetWeatherRequestDTO(longitude=37.61, latitude=55.75)).json()



if __name__ == '__main__':
    print(main())
