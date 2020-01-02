"""INFLUXDB
InfluxDB connector
"""

# # Installed # #
import influxdb

# # Project # #
from ..settings import influx_settings as settings
from ..entities import *
from ..logger import *

__all__ = ("InfluxClient",)


class InfluxClient(influxdb.InfluxDBClient):
    def __init__(self, **kwargs):
        super().__init__(
            host=settings.host,
            port=settings.port,
            database=settings.database,
            username=settings.username,
            password=settings.password,
            **kwargs
        )
        self.create_database(settings.database)
        logger.info(f"Initialized InfluxDB on {settings.host}:{settings.port}")

    def insert(self, *messages: InfluxMessage):
        """Insert messages on Influx
        """
        if messages:
            body = [msg.dict() for msg in messages]
            logger.debug(f"Inserting on Influx (body={body})")
            result: bool = self.write_points(body)
            logger.info(f"Inserted {len(body)} messages on Influx")
            return result
