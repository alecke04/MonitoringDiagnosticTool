# encryption.py
# Utility functions for AES-256 ZIP encryption of diagnostic reports
# Used by NotificationService.encryptReport() and report_generator.encrypt_report()

# TODO: import pyzipper, os
import zipfile

import pyzipper as pyzip
import os


def encrypt_file(file_path: str, password: str) -> str:
    """
    Wraps `file_path` into an AES-256 encrypted, password-protected ZIP archive.
    The original plaintext file is deleted after successful encryption.

    Returns the path to the resulting .zip file.

    # TODO: define archive_path = file_path + ".zip"
    #        open pyzipper.AESZipFile(archive_path, 'w', compression=ZIP_DEFLATED,
    #                                 encryption=WZ_AES)
    #        set zipfile.pwd = password.encode()
    #        write the original file into the archive
    #        close archive
    #        os.remove(file_path) to delete plaintext
    #        return archive_path
    """
    archive_path = file_path + ".zip"
    with pyzip.AESZipFile(archive_path, 'w', compression=pyzip.ZIP_DEFLATED,
                           encryption=pyzip.WZ_AES) as zip_file:
        zip_file.setpassword(password.encode())
        zip_file.write(file_path, os.path.basename(file_path))
    os.remove(file_path)
    return archive_path
    pass


def decrypt_file(archive_path: str, password: str, output_dir: str) -> str:
    """
    Decrypts and extracts a password-protected ZIP archive to `output_dir`.

    Returns the path to the extracted file.

    # TODO: open pyzipper.AESZipFile(archive_path, 'r')
    #        set zipfile.pwd = password.encode()
    #        extractall to output_dir
    #        return path to extracted file
    """
    with pyzip.AESZipFile(archive_path, 'r') as zip_file:
        zip_file.setpassword(password.encode())
        zip_file.extractall(output_dir)
        extracted_files = zip_file.namelist()
        if len(extracted_files) != 1:
            raise ValueError("Expected exactly one file in the archive")
        return os.path.join(output_dir, extracted_files[0])
    pass
