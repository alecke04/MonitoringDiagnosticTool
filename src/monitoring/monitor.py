# MonitoringSystem — core orchestrator class
# Coordinates availability checks, RTT measurement, SSL validation,
# retry logic, and report generation for all monitored servers

from time import time
import time as time_module
import statistics
from datetime import datetime

import requests
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

    def __init__(self, timeout_duration: int = 5, retry_delay_minutes: int = 5, max_retries: int = 3):
        # TODO: assign parameters to self
        # TODO: instantiate self.db = DatabaseHandle(...)
        # TODO: instantiate self.notificationService = NotificationService(...)
        self.timeout_duration = timeout_duration
        self.retry_delay_minutes = retry_delay_minutes
        self.max_retries = max_retries

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
            return True, response
        except Exception as e:
            return False, e

    def measure_rtt(self, url, samples: int = 3) -> list[float]:
        """
        Returns rtt time for 100 requests to specific url

        throws exception if any error is encountered
        """
        measurements = []
        for i in range(samples):
            response = requests.get(url, timeout=self.timeout_duration)
            response.raise_for_status()
            measurements.append(response.elapsed.total_seconds())

        return measurements
'''
    def checkSSL(self, server) -> "SSLResult":
        """
        Retrieves the TLS certificate for server.url and checks expiration.

        Returns SSLResult with isValid and expirationDate.
        # TODO: use ssl and socket stdlib to fetch the cert
        #        compare cert expiry date to today's date
        """
        try:
            import ssl
            import socket
            import datetime
            hostname = server.url.replace("http://", "").replace("https://", "").split("/")[0]
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    expirationDate = cert['notAfter']
                    # Remove GMT suffix before parsing to avoid timezone parsing issues
                    expiry_clean = expirationDate.replace(" GMT", "")
                    exp_date = datetime.datetime.strptime(expiry_clean, "%b %d %H:%M:%S %Y")
                    isValid = exp_date > datetime.datetime.now()
                    return SSLResult(isValid=isValid, expirationDate=expirationDate)
        except Exception as e:
            print(f"Error while checking SSL for {server.url}: {e}")
            return SSLResult(isValid=False, expirationDate=None)
        pass
'''

'''
    def checkAvailability(self, server) -> "AvailResult":
        """
        Sends a single HTTP GET to server.url and returns an AvailResult.

        Returns AvailResult with:
          - isUp=True if status_code < 400
          - isUp=False + httpCode=0 on timeout or connection error
        # TODO: use requests.get with timeout=self.timeout_duration
        #        catch requests.exceptions.Timeout and ConnectionError
        """


        httpCode = 0
        isUp = False

        if not server.url.startswith("http"):
            print(f"Invalid URL for server {server.id}: {server.url}")
            return AvailResult(isUp=False, httpCode=httpCode)
        try:
            response = requests.get(server.url, timeout=self.timeout_duration)
            httpCode = response.status_code
            isUp = httpCode < 400
        except requests.exceptions.Timeout:
            print(f"Timeout while checking availability of {server.url}")
        except requests.exceptions.ConnectionError:
            print(f"Connection error while checking availability of {server.url}")
        return AvailResult(isUp=isUp, httpCode=httpCode)
'''
