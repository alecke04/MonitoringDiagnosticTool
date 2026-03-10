# report_generator.py
# Standalone helpers for building and encrypting diagnostic reports
# The orchestration lives in NotificationService — these are testable standalone units

# TODO: import os, pyzipper (or zipfile for non-encrypted fallback)


def build_report(server, history, failure) -> str:
    """
    Assembles a plain-text diagnostic report from server config,
    failure details, and historical run data.

    Returns the full report as a string.
    # TODO: include sections: server URL, failure timestamp, HTTP status,
    #        SSL status, RTT averages, recent run summary
    """
    pass


def save_report(content: str, output_dir: str = "reports") -> str:
    """
    Saves `content` to a timestamped .txt file inside `output_dir`.

    Returns the file path of the saved report.
    # TODO: generate filename like report_YYYYMMDD_HHMMSS.txt
    #        write content to file and return the path
    """
    pass


def encrypt_report(report_path: str, password: str) -> str:
    """
    Compresses and AES-256 encrypts the file at `report_path` into a ZIP archive.
    Deletes the original plaintext file.

    Returns the path to the .zip archive.
    # TODO: use pyzipper.AESZipFile with ZIP_DEFLATED + WZ_AES
    #        write file into archive with password
    #        delete original file, return archive path
    """
    pass
