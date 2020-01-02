"""EXCEPTIONS
Custom exceptions on the service
"""

__all__ = ("ConfigError", "NoTopicsDefined", "InterruptExceptions")


class ConfigError(Exception):
    """A user-defined configuration is incorrect"""
    pass


class NoTopicsDefined(ConfigError):
    """No configs to subscribe were defined"""
    pass


InterruptExceptions = (KeyboardInterrupt, InterruptedError)
