from sqlalchemy.orm import declarative_base
from src.infrastructure import application_settings

Base = declarative_base()


def build_db_conn_string() -> str:
    db_driver = application_settings.db_driver
    db_user = application_settings.db_user
    db_password = application_settings.db_password
    db_host = application_settings.db_host
    db_port = application_settings.db_port
    db_name = application_settings.db_name
    return f"{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
