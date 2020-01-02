"""LOGGER
Logger instance
"""

# # Native # #
import sys

# # Installed # #
from loguru import logger

# # Package # #
from .settings import system_settings

__all__ = ("logger",)

logger.remove()
logger.add(sys.stderr, level=system_settings.log_level.upper())
