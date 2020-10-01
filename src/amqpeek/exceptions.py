"""Exceptions used in this library."""


class AmqpeekException(Exception):
    """Base exception for library."""

    pass


class ConfigExistsError(AmqpeekException):
    """Attempting to create a configuration file, but it already exists."""

    pass
