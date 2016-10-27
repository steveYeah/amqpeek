class AmqpeekException(Exception):
    """Base exception for library"""
    pass


class ConfigExistsError(AmqpeekException):
    """
    Error thown when attempting to create a
    configuration file, but it already exists
    """
