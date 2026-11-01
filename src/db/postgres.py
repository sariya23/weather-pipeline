import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from src.config import Config

logger = logging.getLogger(__name__)


class PostgresClient:
    def __init__(self, config: Config) -> None:
        self._conn = psycopg2.connect(
            host=config.host,
            port=config.port,
            dbname=config.name,
            user=config.user,
            password=config.password.get_secret_value(),
            cursor_factory=RealDictCursor,
        )

    def close(self) -> None:
        self._conn.close()
        logger.info("Postgres client closed")
