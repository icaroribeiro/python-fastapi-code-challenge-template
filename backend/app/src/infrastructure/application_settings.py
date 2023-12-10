import os


class ApplicationSettings:
    @property
    def http_port(self) -> str:
        return self.get(key="HTTP_PORT", default_value="5000")

    @property
    def db_driver(self) -> str:
        return self.get(key="DB_DRIVER", default_value="postgresql+asyncpg")

    @property
    def db_user(self) -> str:
        return self.get(key="DB_USER", default_value="root")

    @property
    def db_password(self) -> str:
        return self.get(key="DB_PASSWORD", default_value="root")

    @property
    def db_host(self) -> str:
        return self.get(key="DB_HOST", default_value="localhost")

    @property
    def db_port(self) -> str:
        return self.get(key="DB_PORT", default_value="5433")

    @property
    def db_name(self) -> str:
        return self.get(key="DB_NAME", default_value="db")

    @staticmethod
    def get(key, default_value: str = None) -> str:
        return os.getenv(key, default_value)
