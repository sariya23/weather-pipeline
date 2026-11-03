import argparse
import logging
from datetime import UTC, datetime

from geopy.geocoders import Nominatim

import src.lib.log  # noqa
from src.app.app import App, Core, Database
from src.config import Config
from src.place.db.place import PlacePostgres
from src.source.db.source import SourcePostgres
from src.source.models.domain.source import SourceList
from src.weather.api.open_meteo import ApiOpenMeteo
from src.weather.core.weather import WeatherCore
from src.weather.db.weather import WeatherPostgres
from src.weather.models.domain.weather import WeatherList
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO
from src.weather.models.dto.insert_weather import InsertWeatherDTO

logger = logging.getLogger(__name__)


def main(
    config: Config, place_list: list[str], start_date: datetime, end_date: datetime
):
    geolocator = Nominatim(user_agent="weather-pipe")
    open_meteo_api = ApiOpenMeteo(config.base_url)
    weather_measures = WeatherList()
    app = App(
        db=Database(
            weather=WeatherPostgres(config),
            place=PlacePostgres(config),
            source=SourcePostgres(config),
        ),
        core=Core(weather=WeatherCore(weather_api=open_meteo_api)),
    )
    places = app.db.place.all()
    for place in place_list:
        try:
            city, region, country = place.split("/")
        except ValueError as e:
            logger.error(
                "cannot parse (%s) 'city', 'region, 'country' with error '%s', please check format, use city/region/country",
                e,
                place,
            )
            continue
        except Exception as e:
            logger.error("unexpected error while parsing place: %s", e)
            continue
        city_location = geolocator.geocode(f"{city} {region} {country}")
        long, lat = city_location.longitude, city_location.latitude
        req = GetWeatherRequestDTO(
            hourly=[
                "temperature_2m",
                "relative_humidity_2m",
                "rain,wind_speed_10m",
            ],
            longitude=long,
            latitude=lat,
            start_date=start_date,
            end_date=end_date,
        )
        try:
            place = places.get_place(city, region, country)
        except ValueError as e:
            logger.error(
                "cannot get place (%s/%s/%s) with error '%s'", city, region, country, e
            )
            continue
        except Exception as e:
            logger.error("unexpected error while getting place: %s", e)
            continue
        weather_measure = app.core.weather.get_weather(req, place)
        logger.info(
            "success get weather measures for city %s total measures %s",
            city,
            len(weather_measure),
        )
        weather_measures.extend(weather_measure)

    sources = SourceList()
    for source in weather_measures.sources:
        sources.append(app.db.source.get_source_by_name(source))

    to_insert = []
    for weather_measure in weather_measures:
        to_insert.append(
            InsertWeatherDTO(
                place_id=weather_measure.place.id,
                temperature=weather_measure.temperature_cel_2m,
                wind_speed=weather_measure.wind_speed_mm_10m,
                relative_humidity=weather_measure.relative_humidity_2m,
                source_id=sources.get_by_name(weather_measure.source).id,
                measure_timestamp=weather_measure.timestamp,
                rain=weather_measure.rain_mm,
            )
        )
    try:
        app.db.weather.insert_weathers(to_insert)
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WeatherPipeline", description="Pipeline for downloading weather data"
    )
    parser.add_argument("--config", required=True)
    parser.add_argument(
        "--start-date",
        default=datetime.now(tz=UTC).date().strftime("%Y-%m-%d"),
        help="format %Y-%m-%d",
    )
    parser.add_argument(
        "--end-date",
        default=datetime.now(tz=UTC).date().strftime("%Y-%m-%d"),
        help="format %Y-%m-%d",
    )
    args = parser.parse_args()
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    config = Config(_env_file=args.config)
    if config.env == "local":
        logger.setLevel(logging.DEBUG)
    logger.info(
        "Pipeline config: (start_date=%s, end_date=%s env=%s)",
        start_date,
        end_date,
        config.env,
    )
    print(
        main(
            config=config,
            place_list=[
                "Moscow/Moscow/Russia",
                "Kazan/Tatarstan/Russia",
                "Saint Petersburg/Saint Petersburg/Russia",
            ],
            start_date=start_date,
            end_date=end_date,
        )
    )
