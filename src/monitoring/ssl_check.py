# ssl_check.py
# Standalone helper for SSL certificate validation
# The actual orchestration lives in MonitoringSystem.checkSSL()
# This module can be used for unit testing SSL logic in isolation

# TODO: import ssl, socket, datetime


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
    pass
