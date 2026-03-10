# NotificationService — handles report building, encryption, and email delivery
# Triggered by MonitoringSystem.generateSendReport() on failure detection

# TODO: import smtplib, ssl, os, email.mime classes


class NotificationService:
    """
    Builds encrypted diagnostic reports and delivers them via SMTP email.

    Attributes:
        reportPassword (str): Password used to encrypt the ZIP report archive (AES-256)
        senderEmail (str): Gmail (or other SMTP) address used to send alerts
        senderPassword (str): App password / SMTP credential for senderEmail
    """

    def __init__(self, reportPassword: str, senderEmail: str, senderPassword: str):
        # TODO: assign each parameter to self
        pass

    def notifyFailure(self, server, history, failure) -> None:
        """
        Orchestrates the full notification flow for a detected failure:
          1. Build the report text
          2. Save report to a temp file
          3. Encrypt/compress it into a ZIP
          4. Send the email with the ZIP attached

        # TODO: call buildReport → SAVE_TO_FILE → encryptReport → sendEmail
        #        update notification status in DB after sending
        """
        pass

    def buildReport(self, server, history, failure) -> str:
        """
        Compiles server info, failure details, and historical run data
        into a formatted plain-text diagnostic report string.

        Returns the report content as a string.
        # TODO: format sections for: server info, failure details,
        #        recent run history (from history.summarizeRuns()),
        #        RTT stats, SSL status
        """
        pass

    def encryptReport(self, reportPath: str) -> str:
        """
        Compresses `reportPath` into an AES-256 password-protected ZIP archive.
        Deletes the original unencrypted file after archiving.

        Returns the path to the encrypted .zip file.
        # TODO: use pyzipper.AESZipFile to create archive with self.reportPassword
        #        delete the original reportPath file
        #        return archivePath (reportPath + ".zip")
        """
        pass

    def sendEmail(self, to: str, subject: str, body: str, attachmentPath: str) -> None:
        """
        Sends an email via SMTP (STARTTLS) to `to` with the encrypted
        report ZIP attached.

        # TODO: use smtplib.SMTP with STARTTLS on port 587
        #        authenticate with self.senderEmail + self.senderPassword
        #        attach the file at attachmentPath as MIMEApplication
        #        send and close connection
        """
        pass
