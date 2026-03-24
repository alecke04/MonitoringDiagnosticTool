# WebServer model
# Represents a single monitored web server target stored in monitored_targets table


class WebServer:
    """
    Holds the configuration for a monitored web server.

    Attributes:
        id (int): Unique identifier (matches target_id in DB)
        url (str): The server URL to monitor (e.g. https://example.com)
        email (str): Owner's email address for alert notifications
        sample (str): Path to the synthetic 1KB payload used for RTT measurement
    """

    def __init__(self, id: int, url: str, email: str, sample: str):
        # TODO: assign each parameter to self
        self.id = id
        self.url = url
        self.email = email
        self.sample = sample
        pass

    def __repr__(self):
        # TODO: return a readable string like <WebServer id=1 url=...>
        return f"<WebServer id={self.id} url={self.url}>"
