"""RUNNER
Main application execution
"""

# # Project # #
from .exceptions import *
from .services import *
from .logger import *

__all__ = ("run",)


def run():
    redis = RedisClient()
    influx = InfluxClient()
    mqtt = MQTTClient(redis=redis)
    redis2influx = Redis2Influx(redis=redis, influx=influx)

    mqtt.connect()
    mqtt.loop_start()

    try:
        redis2influx.run()
    except InterruptExceptions:
        pass

    mqtt.loop_stop()
    mqtt.disconnect()

    logger.info("Bye!")
