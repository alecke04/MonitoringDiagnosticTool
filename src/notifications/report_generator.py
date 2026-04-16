# report_generator.py
# Standalone helpers for building and encrypting diagnostic reports
# The orchestration lives in NotificationService — these are testable standalone units

# TODO: import os, pyzipper (or zipfile for non-encrypted fallback)


import datetime
import os


def build_report(server, history, run_data) -> str:
    """
    Assembles a plain-text diagnostic report from server config,
    run data, and historical run data.

    Returns the full report as a string.
    # TODO: include sections: server URL, failure timestamp, HTTP status,
    #        SSL status, RTT averages, recent run summary
    """
    server_info = f"Server URL: {server.url}\n"
    timestamp = run_data.timestamp if run_data else "Unknown"
    http_status = run_data.httpStatus if run_data else "Unknown"
    error_desc = run_data.errorDescription if run_data else "Unknown"
    
    failure_info = f"Failure Timestamp: {timestamp}\nHTTP Status: {http_status}\nHTTP Description: {error_desc}\n"
    
    # Handle optional SSL info
    ssl_info = ""
    if run_data and run_data.sslValid is not None:
        ssl_info = f"SSL Valid: {run_data.sslValid}\nSSL Expiration: {run_data.sslExpirationDate}\n"
    
    # Handle optional RTT info
    rtt_info = ""
    if run_data and run_data.avgRTTms:
        rtt_info = f"RTT Average: {run_data.avgRTTms:.2f} ms\nRTT Median: {run_data.medianRTTms:.2f} ms\n"
    
    history_info = f"Recent Run History:\n{history.summarizeRuns()}\n"
    return server_info + failure_info + ssl_info + rtt_info + history_info


def save_report(content: str, output_dir: str = "reports") -> str:
    """
    Saves `content` to a timestamped .txt file inside `output_dir`.

    Returns the file path of the saved report.
    # TODO: generate filename like report_YYYYMMDD_HHMMSS.txt
    #        write content to file and return the path
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.txt"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

def encrypt_report(report_path: str, password: str) -> str:
    """
    Compresses and AES-256 encrypts the file at `report_path` into a ZIP archive.
    Deletes the original plaintext file.

    Returns the path to the .zip archive.
    # TODO: use pyzipper.AESZipFile with ZIP_DEFLATED + WZ_AES
    #        write file into archive with password
    #        delete original file, return archive path
    """
    import pyzipper
    archive_path = report_path + ".zip"
    with pyzipper.AESZipFile(archive_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password.encode())
        zf.write(report_path, os.path.basename(report_path))
    os.remove(report_path)
    return archive_path
