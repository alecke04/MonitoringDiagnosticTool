# report_generator_encrypt.py
# Standalone helpers for building and encrypting diagnostic reports
# The orchestration lives in NotificationService — these are testable standalone units

import os
import pyzipper as pyzip



def build_report(results , server_url , http_code, http_description) -> str:
    """
    Assemble a plain-text diagnostic report and return it as a string.
    """
    lines = [
        "SERVER ERROR REPORT",
        "=" * 50,
        f"Server URL: {server_url}",
        "",
        "Failure Details:",
        f"HTTP Code: {http_code}",
        f"Description: {http_description}",
        "",
        "Previous  Results:",
    ]

    results = list(results)
    if results:
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r}")
    else:
        lines.append("No previous results available.")

    return "\n".join(lines) + "\n"


def write_report(report_text: str, file_path: str) -> str:
    """
    Write the report text to disk and return the file path.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report_text)
    return file_path

def encrypt_file(file_path: str, password: str) -> str:
    """
    Encrypt the file.
    Returns the path to the resulting .zip file.
    """

    archive_path = file_path + ".zip"

    with pyzip.AESZipFile(archive_path, 'w', compression=pyzip.ZIP_DEFLATED, encryption=pyzip.WZ_AES) as zip_file:
        zip_file.setpassword(password.encode("utf-8"))
        zip_file.write(file_path, os.path.basename(file_path))

    os.remove(file_path)
    return archive_path


