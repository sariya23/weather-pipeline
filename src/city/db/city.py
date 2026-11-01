import logging

from src.city.models.domain.city import City
from src.db.postgres import PostgresClient
from src.models.coordinate import Coordinate

logger = logging.getLogger(__name__)


class CityPostgres(PostgresClient):
    def get_city_by_coordinates(self, coordinates: Coordinate) -> City:
        query = "select * from city where longitude=%s and latitude=%s;"
        with self._conn.cursor() as cursor:
            cursor.execute(query, [coordinates.longitude, coordinates.latitude])
            res = cursor.fetchone()

        logger.debug("successfully get city by coordinates %s", res)
        return City(
            id=res["id"],
            city=res["city"],
            coordinates=Coordinate(
                longitude=res["longitude"], latitude=res["latitude"]
            ),
        )
