# NotificationService — handles report building, encryption, and email delivery
# Triggered by MonitoringSystem.generateSendReport() on failure detection

# TODO: import smtplib, ssl, os, email.mime classes


import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from src.notifications.report_generator import save_report, encrypt_report


class NotificationService:
    """
    Builds encrypted diagnostic reports and delivers them via SMTP email.

    Attributes:
        reportPassword (str): Password used to encrypt the ZIP report archive (AES-256)
        senderEmail (str): Gmail (or other SMTP) address used to send alerts
        senderPassword (str): App password / SMTP credential for senderEmail
    """

    def __init__(self, reportPassword: str, senderEmail: str, senderPassword: str, smtpHost: str = "smtp.gmail.com", smtpPort: int = 587, db=None):
        # TODO: assign each parameter to self
        self.reportPassword = reportPassword
        self.senderEmail = senderEmail
        self.senderPassword = senderPassword
        self.smtpHost = smtpHost
        self.smtpPort = smtpPort
        self.db = db

    def notifyFailure(self, server, history, run_id: int) -> None:
        """
        Orchestrates the full notification flow for a detected failure:
          1. Check if we've already notified recently (prevent duplicates)
          2. Query DB for the run data
          3. Build the report text
          4. Save report to a temp file
          5. Encrypt/compress it into a ZIP
          6. Send the email with the ZIP attached
          7. Record notification in DB

        # TODO: call build_report → SAVE_TO_FILE → encryptReport → sendEmail
        #        update notification status in DB after sending
        """
        from src.notifications.report_generator import build_report
        
        try:
            # DEDUPLICATION CHECK: Don't spam if we just notified 15 mins ago
            if self.db and self.db.hasRecentNotification(server.id, minutes_threshold=15):
                print(f"Notification already sent for {server.url} within last 15 minutes. Suppressing duplicate.")
                return
            
            # Fetch the run data from database
            run_data = self.db.getRunById(run_id)
            if not run_data:
                raise Exception(f"Could not find monitoring run {run_id} in database")
            
            report_content = build_report(server, history, run_data)
            report_path = save_report(report_content)
            encrypted_path = encrypt_report(report_path, self.reportPassword)
            subject = f"ALERT: {server.url} is DOWN"
            body = f"Diagnostic report for {server.url} is attached.\n\nPlease review the details and take necessary action."
            self.sendEmail(server.email, subject, body, encrypted_path)
            
            # RECORD SUCCESS: Log notification in DB for deduplication tracking
            if self.db:
                self.db.recordNotification(run_id, filename=os.path.basename(encrypted_path), status='SENT')
            
        except Exception as e:
            print(f"Error during failure notification process: {e}")
            # RECORD FAILURE: Still log it so we know it was attempted
            if self.db:
                try:
                    self.db.recordNotification(run_id, status='FAILED')
                except:
                    pass  # Silent fail on record failure
            raise



    def sendEmail(self, to: str, subject: str, body: str, attachmentPath: str) -> None:
        """
        Sends an email via SMTP (STARTTLS) to `to` with the encrypted
        report ZIP attached.

        # TODO: use smtplib.SMTP with STARTTLS on port 587
        #        authenticate with self.senderEmail + self.senderPassword
        #        attach the file at attachmentPath as MIMEApplication
        #        send and close connection
        """
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = self.senderEmail
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach the encrypted report
            with open(attachmentPath, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachmentPath))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachmentPath)}"'
            msg.attach(part)
            
            # Send the email via SMTP with STARTTLS
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtpHost, self.smtpPort) as server:
                server.starttls(context=context)
                server.login(self.senderEmail, self.senderPassword)
                server.send_message(msg)
            print(f"Alert email sent successfully to {to}")
        except smtplib.SMTPAuthenticationError:
            print(f"SMTP authentication failed. Check SMTP_EMAIL and SMTP_PASSWORD credentials.")
            raise
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred while sending email: {e}")
            raise
        except Exception as e:
            print(f"Failed to send email to {to}: {e}")
            raise
