
from dataclasses import asdict

import psycopg2

from src.config import Config
from src.db.dto.city import City
from src.weather.models.dto.insert_weather import InsertWeatherDTO
import logging

logger = logging.getLogger(__name__)


class PostgresClient:
    def __init__(self, config: Config) -> None:
        self.__conn = psycopg2.connect(
            host=config.host,
            port=config.port,
            dbname=config.name,
            user=config.user,
            password=config.password.get_secret_value()
        )

    def close(self) -> None:
        self.__conn.close()
        logger.info(f"Postgres client closed")

    def __insert_weathers(self, weathers: list[InsertWeatherDTO]):
        insert_query = ("insert into weather (city_id, temperature_cel_2m, wind_speed_10m, relative_humidity_2m, source_id, measure_timestamp) values "
                        "(%(city_id)s, %(temperature)s, %(wind_speed)s, %(relative_humidity)s, %(source_id)s, %(measure_timestamp)s)"
                        "on conflict (city_id, source_id, measure_timestamp) do nothing")
        with self.__conn.cursor() as cursor:
            cursor.executemany(insert_query, [asdict(weather) for weather in weathers])

    def insert_weathers(self, weathers: list[InsertWeatherDTO]):
        try:
            self.__insert_weathers(weathers)
            self.__conn.commit()
            logger.info(f"Successfully inserted {len(weathers)} weathers")
        except Exception as e:
            self.__conn.rollback()
            logger.error(f"Failed to insert {len(weathers)} weathers with exp %s", e)

    def get_city_coordinates(self, long: float, lat: float) -> City:
        query = "select * from city where longitude=%s and latitude=%s;"
        with self.__conn.cursor() as cursor:
            cursor.execute(query, [long, lat])
            res = cursor.fetchone()
        return res




