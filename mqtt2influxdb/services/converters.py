"""CONVERTERS
Helpers to convert/parse between class/data types
"""

# # Native # #
import json
from datetime import datetime

# # Project # #
from ..settings import influx_settings
from ..entities import *

__all__ = ("paho_mqtt_2_mqtt_message", "mqtt_message_2_influx_message", "string_2_mqtt_message", "mqtt_message_2_string")


def paho_mqtt_2_mqtt_message(paho_message: PahoMQTTMessage) -> MQTTMessage:
    return MQTTMessage(
        topic=paho_message.topic,
        payload=paho_message.payload.decode(),
        timestamp=datetime.now().isoformat(timespec="seconds") + "Z",
        qos=paho_message.qos
    )


def mqtt_message_2_influx_message(mqtt_message: MQTTMessage) -> InfluxMessage:
    return InfluxMessage(
        measurement=influx_settings.measurement,
        tags=InfluxTags(topic=mqtt_message.topic, qos=mqtt_message.qos),
        time=mqtt_message.timestamp,
        fields=InfluxFields(payload=mqtt_message.payload)
    )


def string_2_mqtt_message(str_message: str) -> MQTTMessage:
    return MQTTMessage(**json.loads(str_message))


def mqtt_message_2_string(mqtt_message: MQTTMessage, *args, **kwargs) -> str:
    return json.dumps(mqtt_message.dict(*args, **kwargs))
