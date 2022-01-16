from smtplib import SMTP_SSL
from ssl import create_default_context
from typing import NoReturn

from config_loader.config_loader import config


class EmailSender:
    @classmethod
    def send_email(cls, message: str, receiver_email: str) -> NoReturn:

        with SMTP_SSL("smtp.gmail.com", config.SMTP_PORT, context=create_default_context()) as server:
            server.login(config.APPLICATION_EMAIL_ADDRESS, config.APPLICATION_EMAIL_PASSWORD)
            server.sendmail(config.APPLICATION_EMAIL_ADDRESS, receiver_email, message)
