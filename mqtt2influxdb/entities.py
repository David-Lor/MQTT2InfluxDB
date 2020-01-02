"""ENTITIES
Entities used around the project
"""

# # Native # #
import json
import contextlib
from typing import Union, Optional

# # Installed # #
import pydantic
from paho.mqtt.client import MQTTMessage as PahoMQTTMessage

__all__ = ("PahoMQTTMessage", "MQTTMessage", "InfluxMessage", "InfluxFields", "InfluxTags", "RedisInput")


class BaseModel(pydantic.BaseModel):
    def dict(self, *args, **kwargs):
        kwargs.setdefault("exclude_none", True)
        kwargs.setdefault("by_alias", True)
        return super().dict(*args, **kwargs)


class InfluxFields(BaseModel):
    payload: str
    payload_number: Optional[Union[int, float]]
    payload_json: Optional[dict]
    payload_bool: Optional[bool]

    def __init__(self, **kwargs):
        with contextlib.suppress(json.JSONDecodeError):
            payload = json.loads(kwargs["payload"])
            if isinstance(payload, dict):
                kwargs["payload_json"] = payload
            elif isinstance(payload, int) or isinstance(payload, float):
                kwargs["payload_number"] = payload
            elif isinstance(payload, bool):
                kwargs["payload_bool"] = payload

        super().__init__(**kwargs)


class InfluxTags(BaseModel):
    topic: str
    qos: int


class InfluxMessage(BaseModel):
    measurement: str
    tags: InfluxTags
    time: str
    message_fields: InfluxFields = pydantic.Field(None, alias="fields")


class MQTTMessage(BaseModel):
    topic: str
    payload: str
    timestamp: str
    qos: int


RedisInput = Union[str, bytes, int, float]
