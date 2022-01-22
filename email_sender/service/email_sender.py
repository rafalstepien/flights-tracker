from smtplib import SMTP_SSL
from ssl import create_default_context
from typing import NoReturn

from config_loader.config_loader import config

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:

    @staticmethod
    def _message_sender(message: str) -> NoReturn:

        with SMTP_SSL("smtp.gmail.com", config.SMTP_PORT, context=create_default_context()) as server:
            server.login(config.APPLICATION_EMAIL_ADDRESS, config.APPLICATION_EMAIL_PASSWORD)

            for receiver_email in config.RECEIVER_EMAIL:
                server.sendmail(config.APPLICATION_EMAIL_ADDRESS, receiver_email, message)

    @classmethod
    def send_html_email_message(cls, plain_html_message: str) -> NoReturn:

        message = MIMEMultipart("test")
        message["Subject"] = "Daily sumup of the most interesting flights"
        message["From"] = config.APPLICATION_EMAIL_ADDRESS

        html_text = MIMEText(plain_html_message, "html")

        message.attach(html_text)

        EmailSender._message_sender(message=message.as_string())

    @classmethod
    def send_plain_text_email_message(cls, plain_text_message: str):
        EmailSender._message_sender(message=plain_text_message)
