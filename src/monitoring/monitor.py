# MonitoringSystem — core orchestrator class
# Coordinates availability checks, RTT measurement, SSL validation,
# retry logic, and report generation for all monitored servers

from time import time
import time as time_module
import statistics
from datetime import datetime

import requests
from numpy.f2py.auxfuncs import throw_error


#from src.models.results import AvailResult, RTTResult, SSLResult
#from src.models import WebServer
#from src.notifications.email_service import NotificationService
#from src.utils.config import load_config


def _ensure_https(url:str) -> str:
    if url.startswith("https://"):
        return url

    if url.startswith("http://"):
        return "https://" + url[len("http://"):]

    return "https://" + url


class MonitoringSystem:
    """
    Central class that runs the monitoring loop for all registered servers.

    Attributes:
        timeout_duration (int): Max seconds to wait for a server HTTP response
        retry_delay_minutes (int): Base delay in minutes between retry attempts (default 5)
        max_retries (int): How many retry attempts before declaring server down
        db (DatabaseHandle): Database handle instance for persisting results
        notificationService (NotificationService): Service for sending alert emails
    """

    def __init__(self, timeout_duration: int = 1):
        # TODO: assign parameters to self
        # TODO: instantiate self.db = DatabaseHandle(...)
        # TODO: instantiate self.notificationService = NotificationService(...)
        self.timeout_duration = timeout_duration

        #config = load_config()
        
        #self.notificationService = NotificationService(
        #    reportPassword=config.get("REPORT_PASSWORD"),
        #    senderEmail=config.get("SMTP_EMAIL"),
        #    senderPassword=config.get("SMTP_PASSWORD"),
        #    db=self.db
        #)

    def run_check(self, server_address: str) -> tuple[bool, Exception | list[float]]:
        server_address = _ensure_https(server_address)

        try:
            response = self.measure_rtt(server_address)
            print(response)
            return True, response
        except requests.exceptions.SSLError as e:
            return False , Exception(["NONE", "certificate verify failed: certificate has expired" ])
        except requests.exceptions.ConnectTimeout as e:
            return False , Exception(["NONE", "connect timeout"])
        except requests.exceptions.ConnectionError as e:
            return False , Exception(["NONE", "ConnectionError Failed to resolve, Name or service not known "])
        except Exception as e:
            return False, e

    def measure_rtt(self, url, samples: int = 100) -> list[float]:
        """
        Returns rtt time for 100 requests to specific url
        throws exception if any error is encountered
        """
        measurements = []
        for i in range(samples):
            response = requests.get(url, timeout=self.timeout_duration)

            if not (response.status_code in range(200, 299)):
                raise Exception([response.status_code, response.reason])

            measurements.append(response.elapsed.total_seconds())
        return measurements
