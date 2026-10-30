import argparse
import logging
from datetime import datetime

from geopy.geocoders import Nominatim

from src.db.postgres import PostgresClient
from src.config import Config
from src.weather.api.open_meteo import ApiOpenMetio
from src.weather.core.weather import WeatherCore
from src.weather.models.domain.weather import WeatherList
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

def main(config_path: str, city_list: list[str], start_date: datetime, end_date: datetime):
    config = Config(_env_file=config_path)
    geolocator = Nominatim(user_agent="weather-pipe")
    open_meteo_api = ApiOpenMetio(config.base_url)
    weather = WeatherCore(weather_api=[open_meteo_api])
    weather_measures = WeatherList()

    for city in city_list:
        try:
            city_location = geolocator.geocode(city)
            long, lat = city_location.longitude, city_location.latitude
            req = GetWeatherRequestDTO(hourly=['temperature_2m', 'relative_humidity_2m', 'rain,wind_speed_10m'],
                                       longitude=long, latitude=lat, start_date=start_date, end_date=end_date)
            weather_measure = weather.get_weather(req)
            logger.info("success get weather measures for city %s total measures %s", city, len(weather_measure))
            weather_measures.extend(weather_measure)
        except Exception as e:
            logger.error(e)
            continue

    db = PostgresClient(config)
    for i in city_list:
        city_location = geolocator.geocode(i)
        long, lat = city_location.longitude, city_location.latitude
        db.get_city_coordinates(long, lat)
    return weather_measures

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='WeatherPipeline',
                        description='Pipeline for downloading weather data')
    parser.add_argument('config')
    args = parser.parse_args()
    print(main(config_path=args.config,
               city_list=['Moscow', 'Kazan', 'Saint Petersburg'],
               start_date=datetime(2026, 10, 29),
               end_date=datetime(2026, 10, 29)))
