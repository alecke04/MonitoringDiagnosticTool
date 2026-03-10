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
        pass

    def getRuns(self, targetId: int, startTime: str, endTime: str) -> list:
        """
        Returns all runs for a given target filtered by time range.
        # TODO: filter self.runs by startTime and endTime and return matching list
        """
        pass

    def addRun(self, run) -> None:
        """
        Appends a MonitorRun to the history list.
        # TODO: append run to self.runs
        """
        pass

    def getFailureRuns(self) -> list:
        """
        Returns only runs where the server was unreachable or had errors.
        # TODO: filter self.runs where reachable == False and return the list
        """
        pass

    def summarizeRuns(self) -> str:
        """
        Returns a human-readable text summary of all runs in this history window.
        # TODO: build and return a summary string (total, failures, avg RTT, etc.)
        """
        pass
