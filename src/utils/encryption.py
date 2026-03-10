# encryption.py
# Utility functions for AES-256 ZIP encryption of diagnostic reports
# Used by NotificationService.encryptReport() and report_generator.encrypt_report()

# TODO: import pyzipper, os


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
    pass
