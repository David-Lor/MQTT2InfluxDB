"""REDIS2INFLUX
Service to periodically insert data from Redis queue into Influx
"""

# # Native # #
from time import sleep

# # Package # #
from .redis import RedisClient
from .influxdb import InfluxClient
from .converters import *

# # Project # #
from ..settings import influx_settings
from ..exceptions import *
from ..entities import *
from ..logger import *

__all__ = ("Redis2Influx",)


class Redis2Influx:
    redis: RedisClient
    influx: InfluxClient

    def __init__(self, redis: RedisClient, influx: InfluxClient):
        self.redis = redis
        self.influx = influx

    def run(self):
        """Called on the main thread
        """
        while True:
            try:
                sleep(influx_settings.write_freq)
                self._redis2influx()
            except InterruptExceptions as ex:
                raise ex

    def _redis2influx(self):
        """Called periodically to insert messages from the queue into InfluxDB.
        If the messages fail to be inserted, they go back to the queue.
        """
        messages = None

        try:
            messages = self.redis.queue_pop_all()
            logger.debug(f"Read {len(messages)} messages from Redis queue")

            if messages:
                messages_influx = list()
                for message_bytes in messages:
                    message_str = message_bytes.decode()
                    message_mqtt: MQTTMessage = string_2_mqtt_message(message_str)
                    message_influx = mqtt_message_2_influx_message(message_mqtt)
                    messages_influx.append(message_influx)

                self.influx.insert(*messages_influx)

        except Exception as ex:
            if messages:
                self.redis.queue_insert(*messages)
            raise ex
