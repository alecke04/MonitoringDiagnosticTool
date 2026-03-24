# config.py
# Loads environment variables from the .env file using python-dotenv
# All sensitive credentials (SMTP, report password) come from here — never hardcoded

# TODO: from dotenv import load_dotenv
# TODO: import os


def load_config() -> dict:
    """
    Loads and returns the application configuration from environment variables.

    Expected .env keys:
        SMTP_EMAIL       - sender Gmail address
        SMTP_PASSWORD    - app password for SMTP auth
        REPORT_PASSWORD  - password used to encrypt report ZIP archives
        DB_PATH          - path to the SQLite database file (default: data/monitor.db)
        TIMEOUT          - HTTP request timeout in seconds (default: 10)
        RETRY_DELAY      - base retry delay in minutes (default: 5)
        MAX_RETRIES      - max retry attempts before alerting (default: 3)

    Returns a dict with all config values.
    # TODO: call load_dotenv() to read .env file
    #        use os.getenv() for each key with sensible defaults
    #        return the config dict
    """
    # Load environment variables from .env file
    from dotenv import load_dotenv
    import os

    load_dotenv()
    config = {
        "SMTP_EMAIL": os.getenv("SMTP_EMAIL"),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
        "REPORT_PASSWORD": os.getenv("REPORT_PASSWORD"),
        "DB_PATH": os.getenv("DB_PATH", "data/monitor.db"),
        "TIMEOUT": int(os.getenv("TIMEOUT", 10)),
        "RETRY_DELAY": int(os.getenv("RETRY_DELAY", 5)),
        "MAX_RETRIES": int(os.getenv("MAX_RETRIES", 3)),
    }
    return config
    pass
