import os
from logging import config as logging_config
from core.logger import LOGGING
from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn

    class Config:
        env_file = ".env"


app_settings = AppSettings()

logging_config.dictConfig(LOGGING)
PROJECT_NAME = os.getenv('PROGECT_NAME', 'library')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_ROOT', '8000'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
