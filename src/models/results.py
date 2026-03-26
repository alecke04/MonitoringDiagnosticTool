# Result data classes
# Lightweight containers returned by availability, RTT, and SSL checks


class AvailResult:
    """
    Holds the result of an HTTP availability check.

    Attributes:
        isUp (bool): True if server returned a non-error response (status < 400)
        httpCode (int): HTTP status code (0 if connection failed/timed out)
        httpDescript (str): HTTP reason phrase or error description
    """

    def __init__(self, isUp: bool, httpCode: int, httpDescript: str):
        # TODO: assign each parameter to self
        self.isUp = isUp
        self.httpCode = httpCode
        self.httpDescript = httpDescript
        pass

    def __repr__(self):
        # TODO: return readable string like <AvailResult isUp=True code=200>
        return f"<AvailResult isUp={self.isUp} code={self.httpCode}>"
        pass


class RTTResult:
    """
    Holds the results of 100 round-trip time measurements.

    Attributes:
        count (int): Number of measurements taken (typically 100)
        measurements (list): Raw list of individual RTT values in ms
        average (float): Mean RTT across all measurements
        median (float): Median RTT across all measurements
        confidence90Interval (tuple): (lower, upper) bounds of 90% confidence interval
    """

    def __init__(
        self,
        count: int,
        measurements: list,
        average: float,
        median: float,
        confidence90Interval: tuple = None,
    ):
        # TODO: assign each parameter to self
        # confidence90Interval can be None initially; calculated separately
        self.count = count
        self.measurements = measurements
        self.average = average
        self.median = median
        self.confidence90Interval = (None, None)
        pass

    def calculateConfidenceInterval(self) -> None:
        """
        Computes the 90% confidence interval from self.measurements
        and stores it in self.confidence90Interval.
        # TODO: implement using mean, std deviation, and t-distribution or z-score
        """
        n = self.count
        mean = self.average
        stddev = (sum((x - mean) ** 2 for x in self.measurements) / (n - 1)) ** 0.5  # sample standard deviation
        zScore = 1.645  # z-score for 90% confidence
        marginOfError = zScore * (stddev / (n ** 0.5))
        lower = mean - marginOfError
        upper = mean + marginOfError
        self.confidence90Interval = (lower, upper)
        pass

    def __repr__(self):
        # TODO: return readable string like <RTTResult count=100 avg=42.3ms>
        return f"<RTTResult count={self.count} avg={self.average:.2f}ms>"
        pass


class SSLResult:
    """
    Holds the result of an SSL certificate validation check.

    Attributes:
        isValid (bool): True if the certificate exists and has not expired
        expirationDate (str): Expiration date string from the certificate (or "Unknown")
    """

    def __init__(self, isValid: bool, expirationDate: str):
        # TODO: assign each parameter to self
        self.isValid = isValid
        self.expirationDate = expirationDate
        pass

    def __repr__(self):
        # TODO: return readable string like <SSLResult valid=True expires=2027-01-01>
        return f"<SSLResult valid={self.isValid} expires={self.expirationDate}>"
        pass
