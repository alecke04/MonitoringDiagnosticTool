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

    pass
