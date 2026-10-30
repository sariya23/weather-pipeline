from collections.abc import Sequence

import psycopg2

from config import Config



class PostgresClient:
    def __init__(self, config: Config) -> None:
        self.__conn = psycopg2.connect(
            host=config.host,
            port=config.port,
            dbname=config.name,
            user=config.user,
            password=config.password.get_secret_value(),
            autocommit=True,
        )

    def close(self) -> None:
        self.__conn.close()