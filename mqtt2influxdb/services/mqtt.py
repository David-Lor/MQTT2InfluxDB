"""MQTT
MQTT connector
"""

# # Native # #
from typing import List

# # Installed # #
import paho.mqtt.client

# # Package # #
from .redis import RedisClient
from .converters import *

# # Project # #
from ..settings import mqtt_settings as settings
from ..exceptions import *
from ..entities import *
from ..logger import *

__all__ = ("MQTTClient",)


class MQTTClient(paho.mqtt.client.Client):
    topics: List[str]
    redis: RedisClient

    def __init__(self, redis: RedisClient, **kwargs):
        self.redis = redis

        self.topics = settings.subscribe.split(settings.subscribe_separator)
        if not self.topics:
            raise NoTopicsDefined()

        super().__init__(client_id=settings.client_id, **kwargs)

        self.on_connect = self._on_conect_callback
        self.on_disconnect = self._on_disconnect_callback
        self.on_message = self._on_message_callback

    def connect(self, *args, **kwargs):
        logger.info(f"Connecting to MQTT on {settings.broker}:{settings.port}...")
        super().connect(
            host=settings.broker,
            port=settings.port,
            keepalive=settings.keepalive,
            *args, **kwargs
        )

        for topic in self.topics:
            self.subscribe(topic, settings.qos)

    def disconnect(self, *args, **kwargs):
        super().disconnect(*args, **kwargs)

    def subscribe(self, topic, qos=settings.qos, *args, **kwargs):
        super().subscribe(topic, qos, *args, **kwargs)
        logger.debug(f"Subscribed to {topic} (qos={int(qos)})")

    def _on_conect_callback(self, *args):
        logger.info("MQTT connected!")

    def _on_disconnect_callback(self, *args):
        logger.info("MQTT disconnected!")

    def _on_message_callback(self, *args):
        paho_message = next(a for a in args if isinstance(a, PahoMQTTMessage))
        mqtt_message: MQTTMessage = paho_mqtt_2_mqtt_message(paho_message)
        string_message: str = mqtt_message_2_string(mqtt_message)
        # TODO Ensure payload is string and not arbitrary binary data
        # TODO short payload on debug
        logger.debug(f"Rx @ {mqtt_message.topic} : {mqtt_message.payload}")
        self.redis.queue_insert(string_message)
