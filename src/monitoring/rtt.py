# rtt.py
# Standalone helper for RTT measurement
# The actual orchestration lives in MonitoringSystem.measureRTT()
# This module can be used for unit testing RTT logic in isolation

import requests, time, statistics

from src.models.results import RTTResult



def measure(url: str, sample_path: str, samples: int = 100) -> "RTTResult":
    """
    Sends `samples` HTTP GET requests to url + sample_path and
    records the elapsed time of each request in milliseconds.

    Returns an RTTResult with:
      - count = samples
      - measurements = list of individual RTT values
      - average = mean of measurements
      - median = median of measurements
      - confidence90Interval = 90% CI (calculated via RTTResult.calculateConfidenceInterval)

    # TODO: loop `samples` times
    #        record time_before = time.time()
    #        call requests.get(url + sample_path)
    #        record time_after = time.time()
    #        rtt = (time_after - time_before) * 1000  # convert to ms
    #        compute average, median
    #        build and return RTTResult
    """
    measurements = []
    for _ in range(samples):
        time_before = time.time()
        try:
            requests.get(url + sample_path)
            time_after = time.time()
            rtt = (time_after - time_before) * 1000  # convert to ms
            measurements.append(rtt)
        except requests.exceptions.RequestException:
            measurements.append(float('inf'))  # Use infinity to indicate a failed request

    average = statistics.mean(measurements)
    median = statistics.median(measurements)

    return RTTResult(
        count=samples,
        measurements=measurements,
        average=average,
        median=median
    )
    pass