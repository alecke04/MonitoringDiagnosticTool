# availability.py
# Standalone helper for HTTP availability checking
# The actual logic lives in MonitoringSystem.checkAvailability()
# This module can be used for unit testing the check in isolation

# TODO: import requests
import requests
from src.models.results import AvailResult



def check(url: str, timeout: int) -> "AvailResult":
    """
    Sends an HTTP GET request to `url` with the given `timeout`.

    Returns an AvailResult indicating whether the server is up,
    the HTTP status code, and a description.

    # TODO: wrap requests.get in try/except for Timeout and ConnectionError
    #        return AvailResult(isUp, httpCode, httpDescript)
    """
    try:
        response = requests.get(url, timeout=timeout)
        is_up = response.status_code == 200
        return AvailResult(isUp=is_up, httpCode=response.status_code, httpDescript=response.reason)
    except requests.exceptions.Timeout:
        return AvailResult(isUp=False, httpCode=None, httpDescript="Timeout")
    except requests.exceptions.ConnectionError:
        return AvailResult(isUp=False, httpCode=None, httpDescript="Connection Error")
    pass
