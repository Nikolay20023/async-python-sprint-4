import os
from logging import config as logging_config
from core.logger import LOGGING
from pydantic import PostgresDsn, BaseSettings


class AppSettings(BaseSettings):
    app_title: str = 'Short_URL'
    database_dsn: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    class Conffig:
        env_file = '.env'


app_settings = AppSettings()

logging_config.dictConfig(LOGGING)
PROJECT_NAME = os.getenv('PROGECT_NAME', 'library')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_ROOT', '8000'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
