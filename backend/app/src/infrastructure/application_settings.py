import os
from typing import Optional


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

    # @property
    # def max_content_size(self) -> str:
    #     return self.get(key="MAX_CONTENT_SIZE", default_value="1048576")

    @property
    def upload_folder(self) -> str:
        return self.get(key="UPLOAD_FOLDER", default_value="./../uploads")

    @property
    def allowed_extensions(self) -> str:
        return self.get(key="ALLOWED_EXTENSIONS", default_value="txt")

    @property
    def max_line_length(self) -> str:
        return self.get(key="MAX_LINE_LENGTH", default_value="86")

    @property
    def minimum_page_number(self) -> str:
        return self.get(key="MINIMUM_PAGE_NUMBER", default_value="1")

    @property
    def minimum_page_size(self) -> str:
        return self.get(key="MINIMUM_PAGE_SIZE", default_value="5")

    @property
    def maximum_page_size(self) -> str:
        return self.get(key="MAXIMUM_PAGE_SIZE", default_value="20")

    @property
    def public_key_file_path(self) -> str:
        return self.get(
            key="PUBLIC_KEY_FILE_PATH", default_value="./config/jwtRS256.key.pub"
        )

    @property
    def private_key_file_path(self) -> str:
        return self.get(
            key="PRIVATE_KEY_FILE_PATH", default_value="./config/jwtRS256.key"
        )

    @property
    def access_token_expiration_time_in_seconds(self) -> str:
        return self.get(
            key="ACCESS_TOKEN_EXPIRATION_TIME_IN_SECONDS", default_value="3600"
        )

    @property
    def refresh_token_expiration_time_in_seconds(self) -> str:
        return self.get(
            key="REFRESH_TOKEN_EXPIRATION_TIME_IN_SECONDS", default_value="86400"
        )

    # @property
    # def max_transaction_file_content_size(self) -> str:
    #     return self.get(key="MAX_CONTENT_SIZE", default_value="1048576")

    @staticmethod
    def get(key, default_value: str = None) -> str:
        return os.getenv(key, default_value)
