import logging

from src.db.postgres import PostgresClient
from src.place.models.domain.place import Place, PlaceList

logger = logging.getLogger(__name__)


class PlacePostgres(PostgresClient):
    def get_city(self, region: str, country: str, city: str) -> Place:
        query = (
            "select p.id, city, r.region, c.country from place p join region r on p.region_id = r.id join country c on c.id = p.country_id "
            "where p.region = %s and p.country = %s and p.city = %s;"
        )
        with self._conn.cursor() as cursor:
            cursor.execute(query, [region, country, city])
            res = cursor.fetchone()

        logger.debug("successfully get city %s", res)
        return Place(
            id=res["id"], city=res["city"], region=res["region"], country=res["country"]
        )

    def all(self) -> PlaceList:
        with self._conn.cursor() as cursor:
            cursor.execute("select p.id, city, r.region, c.country from place p join region r on p.region_id = r.id join country c on c.id = p.country_id;")
            res = cursor.fetchall()
        return PlaceList(
            Place(id=p["id"], city=p["city"], region=p["region"], country=p["country"])
            for p in res
        )
