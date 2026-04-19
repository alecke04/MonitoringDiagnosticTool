# ssl_check.py
# Standalone helper for SSL certificate validation
# The actual orchestration lives in MonitoringSystem.checkSSL()
# This module can be used for unit testing SSL logic in isolation

import ssl, socket, datetime

from src.models.results import SSLResult


def check(url: str) -> "SSLResult":
    """
    Connects to the host extracted from `url` on port 443 and retrieves
    the TLS certificate. Compares the expiration date to today.

    Returns SSLResult with:
      - isValid = True if certificate exists and has not expired
      - expirationDate = cert expiry date string, or "Unknown" on error

    # TODO: parse hostname from url (strip https://)
    #        use ssl.create_default_context() and socket to fetch cert
    #        parse cert["notAfter"] and compare to datetime.date.today()
    #        catch ssl.SSLError and return SSLResult(isValid=False, "Unknown")
    """
    url = url.replace("https://", "").split("/")[0]  # Extract hostname
    try:
        context = ssl.create_default_context()
        with socket.create_connection((url, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                cert = ssock.getpeercert()
                expiry_str = cert.get("notAfter", "Unknown")
                if expiry_str == "Unknown":
                    return SSLResult(isValid=False, expirationDate="Unknown")
                # Remove GMT suffix before parsing to avoid timezone parsing issues
                expiry_clean = expiry_str.replace(" GMT", "")
                expiry_date = datetime.datetime.strptime(expiry_clean, "%b %d %H:%M:%S %Y").date()
                is_valid = expiry_date > datetime.date.today()
                return SSLResult(isValid=is_valid, expirationDate=expiry_str)

    except ssl.SSLError:
        return SSLResult(isValid=False, expirationDate="Unknown")
    def run_check(self, server_address: str) -> None:

        server_address = _ensure_https(server_address)

        # if up: measure RTT + validate SSL, save to DB
        avail_result = self.checkAvailability(server_address)
            if avail_result.isUp:
                rttResult = self.measureRTT(server_address)
                sslResult = self.checkSSL(server_address)

                if not sslResult.isValid:
                    print(f"SSL certificate for {server_address} is invalid. Generating report.")
                    self.generateSendReport(server_address, run_id)
            else:
                print(f"{server_address} is down. Retrying with increasing frequency.")
                retryResult = self.waitRetryAvailability(server_address)
                if retryResult.isUp:
                    print(f"{server_address} is back up after retry. Saving result to DB.")
                else:
                    print(f"{server_address} is still down after retries. Generating report.")
                    run_id = self.db.saveResult(server_address, retryResult, None, None)
                    self.generateSendReport(server_address, run_id)
        pass
    pass
