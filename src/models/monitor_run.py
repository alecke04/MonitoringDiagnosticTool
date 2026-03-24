# MonitorRun model
# Represents a single monitoring cycle result (one row in monitored_runs table)


class MonitorRun:
    """
    Stores results from one complete monitoring cycle for a specific server.

    Attributes:
        runId (int): Unique run identifier (matches run_id in DB)
        timestamp (str): ISO 8601 datetime of when this run occurred
        reachable (bool): True if the server responded successfully
        httpStatus (int): HTTP response code (e.g. 200, 404, 0 for timeout)
        errorDescription (str): Human-readable error label if any
        sslValid (bool): True if the SSL certificate is valid and not expired
        sslExpirationDate (str): SSL cert expiration date string
        avgRTTms (float): Average of 100 RTT measurements in milliseconds
        medianRTTms (float): Median of 100 RTT measurements in milliseconds
        confidence90Interval (tuple): (lower, upper) 90% confidence interval for RTT
    """

    def __init__(
        self,
        runId: int,
        timestamp: str,
        reachable: bool,
        httpStatus: int,
        errorDescription: str,
        sslValid: bool,
        sslExpirationDate: str,
        avgRTTms: float,
        medianRTTms: float,
        confidence90Interval: tuple,
    ):
        # TODO: assign each parameter to self
        self.runId = runId
        self.timestamp = timestamp
        self.reachable = reachable
        self.httpStatus = httpStatus
        self.errorDescription = errorDescription
        self.sslValid = sslValid
        self.sslExpirationDate = sslExpirationDate
        self.avgRTTms = avgRTTms
        self.medianRTTms = medianRTTms
        self.confidence90Interval = confidence90Interval
        pass

    def __repr__(self):
        # TODO: return a readable string like <MonitorRun id=1 reachable=True>
        return f"<MonitorRun id={self.runId} reachable={self.reachable}>"
        pass
