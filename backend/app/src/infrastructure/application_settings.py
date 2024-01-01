import os


class ApplicationSettings:
    @property
    def http_port(self) -> str:
        return self.get(key="HTTP_PORT", default_value="5000")

    @property
    def database_driver(self) -> str:
        return self.get(key="DATABASE_DRIVER", default_value="postgresql+asyncpg")

    @property
    def database_user(self) -> str:
        return self.get(key="DATABASE_USER", default_value="root")

    @property
    def database_password(self) -> str:
        return self.get(key="DATABASE_PASSWORD", default_value="root")

    @property
    def database_host(self) -> str:
        return self.get(key="DATABASE_HOST", default_value="localhost")

    @property
    def database_port(self) -> str:
        return self.get(key="DATABASE_PORT", default_value="5433")

    @property
    def database_name(self) -> str:
        return self.get(key="DATABASE_NAME", default_value="db")

    @property
    def database_url(self) -> str:
        return self.get(
            key="DATABASE_URL",
            default_value="postgresql+asyncpg://root:root@localhost:5433/db",
        )

    @staticmethod
    def get(key, default_value: str = None) -> str:
        return os.getenv(key, default_value)
