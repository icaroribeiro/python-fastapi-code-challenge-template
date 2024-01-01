from sqlalchemy.orm import declarative_base
from src.infrastructure import application_settings

Base = declarative_base()


def get_database_url() -> str:
    database_url = application_settings.database_url
    return database_url
