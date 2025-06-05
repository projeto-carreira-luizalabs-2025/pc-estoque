class HealthCheckException(Exception):
    message_type = "unknown error"

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.message_type, self.message)


class InvalidConfigurationException(HealthCheckException):
    message_type = "unexpected configuration"


class ServiceWarning(HealthCheckException):
    """
    Warning of service misbehavior.

    If the ``HEALTH_CHECK['WARNINGS_AS_ERRORS']`` is set to ``False``,
    these exceptions will not case a 500 status response.
    """

    message_type = "warning"


class ServiceUnavailable(HealthCheckException):
    message_type = "unavailable"


class ServiceReturnedUnexpectedResult(HealthCheckException):
    message_type = "unexpected result"


__all__ = [
    "HealthCheckException",
    "ServiceWarning",
    "ServiceUnavailable",
    "ServiceReturnedUnexpectedResult",
]
