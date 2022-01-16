import os

from pydantic import BaseSettings


class ConfigLoader(BaseSettings):

    BASE_AZAIR_URL: str = ""
    SMTP_PORT: int = 465
    APPLICATION_EMAIL_PASSWORD: str = ""
    APPLICATION_EMAIL_ADDRESS: str = ""
    RECEIVER_EMAIL: str = ""
    TIMEOUT: int = 10

    class Config:
        env_file = os.environ.get("ENV_FILE")


config = ConfigLoader()
