import logging

from src.db.postgres import PostgresClient
from src.place.models.domain.place import Place, PlaceList

logger = logging.getLogger(__name__)


class PlacePostgres(PostgresClient):
    def all(self) -> PlaceList:
        with self._conn.cursor() as cursor:
            cursor.execute("select p.id, city, r.region, c.country from place p join region r on p.region_id = r.id join country c on c.id = p.country_id;")
            res = cursor.fetchall()
        return PlaceList(
            Place(id=p["id"], city=p["city"], region=p["region"], country=p["country"])
            for p in res
        )
