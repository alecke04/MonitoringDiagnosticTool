# MonitoringSystem — core orchestrator class
# Coordinates availability checks, RTT measurement, SSL validation,
# retry logic, and report generation for all monitored servers

from time import time

import requests
from src.models.results import AvailResult, RTTResult, SSLResult, SSLResult
from src.models import WebServer
from src.database.db_handle import DatabaseHandle
from src.notifications.email_service import NotificationService


class MonitoringSystem:
    """
    Central class that runs the monitoring loop for all registered servers.

    Attributes:
        timeoutDuration (int): Max seconds to wait for a server HTTP response
        retryDelayMinutes (int): Base delay in minutes between retry attempts (default 5)
        maxRetries (int): How many retry attempts before declaring server down
        db (DatabaseHandle): Database handle instance for persisting results
        notificationService (NotificationService): Service for sending alert emails
    """

    def __init__(self, timeoutDuration: int, retryDelayMinutes: int = 5, maxRetries: int = 3):
        # TODO: assign parameters to self
        # TODO: instantiate self.db = DatabaseHandle(...)
        # TODO: instantiate self.notificationService = NotificationService(...)
        self.timeoutDuration = timeoutDuration
        self.retryDelayMinutes = retryDelayMinutes
        self.maxRetries = maxRetries

        self.db = DatabaseHandle()
        self.notificationService = NotificationService()

    def runCheck(self) -> None:
        """
        Main loop — iterates over all monitored servers and runs a full check cycle.
        Called on each scheduled interval by the scheduler in main.py.

        For each server:
          - Check availability
          - If up: measure RTT + validate SSL, save to DB
          - If down: retry with increasing frequency
          - If still down after retries: save failure + trigger report
          - If SSL invalid: trigger report even when reachable
        # TODO: implement loop using checkAvailability, measureRTT, checkSSL,
        #        waitRetryAvailability, generateSendReport, db.saveResult
        """
        if not self.db:
            print("Database connection not established.")
            return
        else:
            print("Database connection established.")

        #check if there are any servers to monitor
        servers = self.db.getMonitoredServers()
        if not servers:
            print("No servers to monitor.")
            return
        else:
            print(f"Monitoring {len(servers)} servers.")
        
        # if up: measure RTT + validate SSL, save to DB
        for server in servers:
                availResult = self.checkAvailability(server)
                if availResult.isUp:
                    rttResult = self.measureRTT(server)
                    sslResult = self.checkSSL(server)
                    self.db.saveResult(server, availResult, rttResult, sslResult)
    
                    if not sslResult.isValid:
                        print(f"SSL certificate for {server.url} is invalid. Generating report.")
                        self.generateSendReport(server, "SSL certificate invalid")
                else:
                    print(f"{server.url} is down. Retrying with increasing frequency.")
                    retryResult = self.waitRetryAvailability(server)
                    if retryResult.isUp:
                        print(f"{server.url} is back up after retry. Saving result to DB.")
                        self.db.saveResult(server, retryResult, None, None)
                    else:
                        print(f"{server.url} is still down after retries. Generating report.")
                        self.db.saveResult(server, retryResult, None, None)
                        self.generateSendReport(server, "Server down after retries")
        pass

    def checkAvailability(self, server) -> "AvailResult":
        """
        Sends a single HTTP GET to server.url and returns an AvailResult.

        Returns AvailResult with:
          - isUp=True if status_code < 400
          - isUp=False + httpCode=0 on timeout or connection error
        # TODO: use requests.get with timeout=self.timeoutDuration
        #        catch requests.exceptions.Timeout and ConnectionError
        """
        httpCode = 0
        isUp = False

        if not server.url.startswith("http"):
            print(f"Invalid URL for server {server.id}: {server.url}")
            return AvailResult(isUp=False, httpCode=httpCode)
        try:
            response = requests.get(server.url, timeout=self.timeoutDuration)
            httpCode = response.status_code
            isUp = httpCode < 400
        except requests.exceptions.Timeout:
            print(f"Timeout while checking availability of {server.url}")
        except requests.exceptions.ConnectionError:
            print(f"Connection error while checking availability of {server.url}")
        return AvailResult(isUp=isUp, httpCode=httpCode)

    def measureRTT(self, server, samples: int = 100) -> "RTTResult":
        """
        Sends `samples` HTTP GET requests to server.url + server.sample
        and records the round-trip time of each.

        Returns RTTResult with count, measurements list, average, median,
        and 90% confidence interval.
        # TODO: loop samples times, record time before/after each GET
        #        compute average, median, call calculateConfidenceInterval()
        """
        samples = 100
        measurements = []
        get_url = server.url + server.sample
        for i in range(samples):
            try:
                start_time = time.time()
                response = requests.get(get_url, timeout=self.timeoutDuration)
                end_time = time.time()
                rtt = end_time - start_time
                measurements.append(rtt)
            except requests.exceptions.Timeout:
                print(f"Timeout while measuring RTT for {server.url} (sample {i+1}/{samples})")
            except requests.exceptions.ConnectionError:
                print(f"Connection error while measuring RTT for {server.url} (sample {i+1}/{samples})")
        return RTTResult(count=len(measurements), measurements=measurements)
        pass

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
            hostname = server.url.replace("http://", "").replace("https://", "").split("/")[0]
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    expirationDate = cert['notAfter']
                    from datetime import datetime
                    exp_date = datetime.strptime(expirationDate, "%b %d %H:%M:%S %Y %Z")
                    isValid = exp_date > datetime.now()
                    return SSLResult(isValid=isValid, expirationDate=expirationDate)
        except Exception as e:
            print(f"Error while checking SSL for {server.url}: {e}")
            return SSLResult(isValid=False, expirationDate=None)
        pass

    def waitRetryAvailability(self, server) -> "AvailResult":
        """
        Retries checkAvailability up to maxRetries times with decreasing wait intervals.

        Wait time per attempt = (retryDelayMinutes * 60) / attempt
        so retries get progressively faster (increased monitoring frequency).

        Returns the first successful AvailResult, or a failure AvailResult
        with httpCode=404 after all retries are exhausted.
        # TODO: loop 1..maxRetries, WAIT decreasing seconds, call checkAvailability
        """
        
        pass

    def generateSendReport(self, server, failure) -> None:
        """
        Fetches the 50 most recent runs for this server from the DB,
        then hands off to notificationService.notifyFailure to build
        and send the encrypted diagnostic email.
        # TODO: call db.getRecent(number=50, server=server)
        #        call notificationService.notifyFailure(server, history, failure)
        """
        pass
