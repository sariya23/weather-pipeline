import logging

from src.db.postgres import PostgresClient
from src.source.models.domain.source import Source

logger = logging.getLogger(__name__)


class SourcePostgres(PostgresClient):
    def get_source_by_name(self, name: str) -> Source:
        query = "select * from source where source_name=%s;"
        with self._conn.cursor() as cursor:
            cursor.execute(query, [name])
            res = cursor.fetchone()
        logger.debug("successfully get source by name %s", res)
        return Source(
            id=res["id"],
            source_name=res["source_name"],
            source_url=res.get("source_url"),
        )
