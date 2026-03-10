# availability.py
# Standalone helper for HTTP availability checking
# The actual logic lives in MonitoringSystem.checkAvailability()
# This module can be used for unit testing the check in isolation

# TODO: import requests


def check(url: str, timeout: int) -> "AvailResult":
    """
    Sends an HTTP GET request to `url` with the given `timeout`.

    Returns an AvailResult indicating whether the server is up,
    the HTTP status code, and a description.

    # TODO: wrap requests.get in try/except for Timeout and ConnectionError
    #        return AvailResult(isUp, httpCode, httpDescript)
    """
    pass
