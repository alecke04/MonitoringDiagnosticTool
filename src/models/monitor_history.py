# MonitorHistory model
# Holds a collection of MonitorRun objects for a specific server over a time window


class MonitorHistory:
    """
    Aggregates historical monitoring runs for a specific server target.

    Attributes:
        targetId (int): References the server (matches target_id in DB)
        url (str): The server URL this history belongs to
        emailRecipient (str): Email address for notifications
        startTime (str): Start of the history window (ISO 8601)
        endTime (str): End of the history window (ISO 8601)
        runs (list): List of MonitorRun objects within the window
    """

    def __init__(
        self,
        targetId: int,
        url: str,
        emailRecipient: str,
        startTime: str,
        endTime: str,
    ):
        # TODO: assign parameters and initialize self.runs as an empty list
        self.targetId = targetId
        self.url = url
        self.emailRecipient = emailRecipient
        self.startTime = startTime
        self.endTime = endTime
        self.runs = []
        pass

    def getRuns(self, targetId: int, startTime: str, endTime: str) -> list:
        """
        Returns all runs for a given target filtered by time range.
        # TODO: filter self.runs by startTime and endTime and return matching list
        """
        return [run for run in self.runs if self.startTime <= run.timestamp <= self.endTime]
        pass

    def addRun(self, run) -> None:
        """
        Appends a MonitorRun to the history list.
        # TODO: append run to self.runs
        """
        self.runs.append(run)
        pass

    def getFailureRuns(self) -> list:
        """
        Returns only runs where the server was unreachable or had errors.
        # TODO: filter self.runs where reachable == False and return the list
        """
        return [run for run in self.runs if not run.reachable]
        pass

    def summarizeRuns(self) -> str:
        """
        Returns a human-readable text summary of all runs in this history window.
        # TODO: build and return a summary string (total, failures, avg RTT, etc.)
        """
        totalRuns = len(self.runs)
        failureRuns = len(self.getFailureRuns())
        avgRTT = sum(run.avgRTTms for run in self.runs) / totalRuns if totalRuns > 0 else 0
        summary = (
            f"MonitorHistory for {self.url} from {self.startTime} to {self.endTime}:\n"
            f"Total Runs: {totalRuns}\n"
            f"Failures: {failureRuns}\n"
            f"Average RTT: {avgRTT:.2f} ms\n"
        )
        return summary
        pass
