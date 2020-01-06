"""SETTINGS HANDLER
Load settings from dotenv file or environment variables
"""

# # Native # #
import uuid
from typing import Optional

# # Installed # #
from dotenv_settings_handler import BaseSettingsHandler
from dotenv import load_dotenv

__all__ = ("mqtt_settings", "influx_settings", "redis_settings", "system_settings")

client_id = '-'.join(str(uuid.uuid1()).split('-')[1:])


class BaseSettings(BaseSettingsHandler):
    class Config:
        case_insensitive = True


class MQTTSettings(BaseSettings):
    broker: str = "localhost"
    port: int = 1883
    subscribe: str = "#"
    subscribe_separator: str = ","
    client_id: str = "MQTT2InfluxDB_" + client_id
    keepalive: int = 60
    qos: int = 0
    username: Optional[str]
    password: Optional[str]
    ssl: bool = False
    ca_cert_file: Optional[str]
    cert_file: Optional[str]
    key_file: Optional[str]

    class Config(BaseSettings.Config):
        env_prefix = "MQTT_"


class InfluxSettings(BaseSettings):
    host: str = "localhost"
    port: int = 8086
    username: Optional[str]
    password: Optional[str]
    database: str = "mqtt2influxdb"
    measurement: str = "mqtt"
    write_freq: float = 60

    class Config(BaseSettings.Config):
        env_prefix = "INFLUX_"


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    queue_name: str = "mqtt2influxdb_" + client_id

    class Config(BaseSettings.Config):
        env_prefix = "REDIS_"


class SystemSettings(BaseSettings):
    log_level: str = "INFO"


load_dotenv()

mqtt_settings = MQTTSettings()
influx_settings = InfluxSettings()
redis_settings = RedisSettings()
system_settings = SystemSettings()
