import logging
from dataclasses import asdict

from src.db.postgres import PostgresClient
from src.weather.models.dto.insert_weather import InsertWeatherDTO

logger = logging.getLogger(__name__)

class WeatherPostgres(PostgresClient):
    def __insert_weathers(self, weathers: list[InsertWeatherDTO]):
        insert_query = (
            "insert into weather (place_id, temperature_cel_2m, wind_speed_ms_10m, relative_humidity_2m, source_id, measure_timestamp, rain_mm) values "
            "(%(place_id)s, %(temperature)s, %(wind_speed)s, %(relative_humidity)s, %(source_id)s, %(measure_timestamp)s, %(rain)s)"
            "on conflict (place_id, source_id, measure_timestamp) do nothing"
        )
        with self._conn.cursor() as cursor:
            cursor.executemany(insert_query, [asdict(weather) for weather in weathers])

    def insert_weathers(self, weathers: list[InsertWeatherDTO]):
        try:
            self.__insert_weathers(weathers)
            self._conn.commit()
            logger.info(f"Successfully inserted {len(weathers)} weathers")
        except Exception as e:
            self._conn.rollback()
            logger.error(f"Failed to insert {len(weathers)} weathers with exp '%s'", e)