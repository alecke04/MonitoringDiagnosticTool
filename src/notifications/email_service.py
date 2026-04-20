# NotificationService — handles report building, encryption, and email delivery
# Triggered by MonitoringSystem.generateSendReport() on failure detection

# TODO: import smtplib, ssl, os, email.mime classes


import os
import smtplib
import ssl
from email import encoders

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

from .report_generator_encrypt import *


class NotificationService:
    """
    Builds encrypted diagnostic reports and delivers them via SMTP email.

    Attributes:
        senderEmail (str): Gmail address used to send alerts
        senderPassword (str): App password
    """

    def __init__(self):
        load_dotenv()
        self.SenderEmail = os.getenv("GMAIL_SENDER")
        self.SenderPassword = os.getenv("GMAIL_SENDER_PASSWORD")
        self.ReceiverEmail = ['pjark.sander@gmail.com']
        self.File_Password = os.getenv("FILE_PASSWORD")


    def generate_and_send_report(self, results,server_url, http_code, http_description,subject = "Server Failure Report",) -> str:
        """
        build, encrypt and send the report
        """



        report_text = build_report( results,server_url,http_code, http_description,)
        report_path = write_report(report_text, "server_report.txt")
        zip_path = encrypt_file(report_path, self.File_Password)

        self.sendEmail(subject, self.ReceiverEmail, zip_path)
        #return zip_path


    def sendEmail(self, subject, recipients, report_file) -> None:
        """
        Sends an email via SMTP (STARTTLS) to `to` with the encrypted
        report ZIP attached.

        #        authenticate with self.senderEmail + self.senderPassword
        #        attach the file at attachmentPath as MIMEApplication
        #        send and close connection
        """

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.SenderEmail
        msg['To'] =  ', '.join(self.ReceiverEmail)


        with open(report_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            f"attachment; filename={report_file}", )
            msg.attach(part)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(self.SenderEmail, self.SenderPassword)
                server.sendmail(self.SenderEmail, recipients, msg.as_string())
            os.remove(report_file)
        except Exception as e:
            print(f"Error: {e}")
