"""REDIS
Redis connector
"""

# # Native # #
from typing import List

# # Installed # #
import redis

# # Project # #
from ..settings import redis_settings as settings
from ..entities import *
from ..logger import *

__all__ = ("RedisClient",)


class RedisClient(redis.Redis):
    def __init__(self, **kwargs):
        super().__init__(
            host=settings.host,
            port=settings.port,
            db=settings.db,
            **kwargs
        )
        logger.info(f"Initialized Redis on {settings.host}:{settings.port}")

    def queue_insert(self, *data: RedisInput, key=settings.queue_name):
        count = self.rpush(key, *data)
        logger.debug(f"Inserted into Redis queue (count={count})")
        return count

    def queue_pop_all(self, key=settings.queue_name) -> List[bytes]:
        data = self.lrange(key, 0, -1)
        self.delete(key)
        logger.debug(f"Retrieved {len(data)} items from Redis queue")
        return data
