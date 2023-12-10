from datetime import datetime, timedelta
from uuid import uuid4

from fastapi.logger import logger

from src.domain.model.auth import Auth
from src.domain.model.token_schema import TokenSchema
from src.domain.repository.auth import AuthRepository
from src.infrastructure import application_settings
from src.infrastructure.jwt.jwt_auth import JWTAuth
from src.infrastructure.jwt.jwt_payload import JWTPayload
from src.utils.api_exceptions import ServerErrorException, UnauthorizedException
from src.utils.datetime import datetime_to_integer_timestamp
from src.utils.security import get_hashed_password, verify_password


class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        jwt_auth: JWTAuth,
    ):
        self.__auth_repository = auth_repository
        self.__jwt_auth = jwt_auth

    async def save_auth(self, auth: Auth) -> Auth:
        return await self.__auth_repository.create_auth(auth=auth)

    async def sign_in(
        self, username: str, password: str, current_datetime: datetime
    ) -> TokenSchema:
        auth = await self.__auth_repository.get_auth_by_username(username=username)

        if not auth:
            logger.error(msg=f"Auth with username={username} not exists.")
            raise UnauthorizedException(
                extra=f"Username={username} is incorrect. Try again."
            )

        is_authenticated = verify_password(
            plain_password=password, hashed_password=auth.password
        )

        if not is_authenticated:
            logger.error(
                msg=f"Auth with username={username} and password={password} not exists."
            )
            raise UnauthorizedException(extra="Password is incorrect. Try again.")

        new_login_id = str(uuid4())

        access_token_expires_delta = timedelta(
            minutes=int(application_settings.access_token_expires_in)
        )

        access_token = self._build_token(
            auth_id=str(auth.id),
            login_id=new_login_id,
            current_datetime=current_datetime,
            expires_delta=access_token_expires_delta,
        )

        refresh_token_expires_delta = timedelta(
            minutes=int(application_settings.refresh_token_expires_in)
        )

        jwt_payload_of_refresh_token = self._build_jwt_payload(
            auth_id=str(auth.id),
            login_id=new_login_id,
            current_datetime=current_datetime,
            expires_delta=refresh_token_expires_delta,
        )

        refresh_token = self.jwt_auth.create_jwt_signed_with_rs256_algorithm(
            private_key_file_path=application_settings.private_key_file_path,
            jwt_payload=jwt_payload_of_refresh_token,
        )

        auth.login_id = new_login_id

        auth.refresh_token_id = jwt_payload_of_refresh_token.jti

        await self.auth_repository.update_auth(auth=auth)

        if not auth:
            logger.error(f"Auth={auth} not updated when performing sign in operation.")
            raise ServerErrorException(extra="Auth not updated")

        return TokenSchema(
            access_token=access_token,
            access_token_expires_in=datetime_to_integer_timestamp(
                dt=current_datetime + access_token_expires_delta
            ),
            refresh_token=refresh_token,
            refresh_token_expires_in=jwt_payload_of_refresh_token.exp,
        )

    async def renew_token(self, token: str, current_datetime: datetime) -> TokenSchema:
        jwt_payload = self.jwt_auth.verify_jwt_signed_with_rs256_algorithm(
            public_key_file_path=application_settings.public_key_file_path,
            token=token,
        )

        access_token_expires_delta = timedelta(
            minutes=int(application_settings.access_token_expires_in)
        )

        access_token = self._build_token(
            auth_id=jwt_payload.auth_id,
            login_id=jwt_payload.login_id,
            current_datetime=current_datetime,
            expires_delta=access_token_expires_delta,
        )

        refresh_token_expires_delta = timedelta(
            minutes=int(application_settings.refresh_token_expires_in)
        )

        jwt_payload_of_refresh_token = self._build_jwt_payload(
            auth_id=jwt_payload.auth_id,
            login_id=jwt_payload.login_id,
            current_datetime=current_datetime,
            expires_delta=refresh_token_expires_delta,
        )

        refresh_token = self.jwt_auth.create_jwt_signed_with_rs256_algorithm(
            private_key_file_path=application_settings.private_key_file_path,
            jwt_payload=jwt_payload_of_refresh_token,
        )

        auth = await self.auth_repository.update_auth_refresh_token_id(
            id=jwt_payload.auth_id,
            old_refresh_token_id=jwt_payload.jti,
            new_refresh_token_id=jwt_payload_of_refresh_token.jti,
        )

        if not auth:
            logger.error(
                msg=f"Auth with refresh token id={jwt_payload.jti} not exists."
            )
            raise UnauthorizedException(extra="Refresh token is incorrect. Try again.")

        return TokenSchema(
            access_token=access_token,
            access_token_expires_in=datetime_to_integer_timestamp(
                dt=current_datetime + access_token_expires_delta
            ),
            refresh_token=refresh_token,
            refresh_token_expires_in=jwt_payload_of_refresh_token.exp,
        )

    async def sign_out(self, auth_id: str, login_id: str) -> None:
        auth = await self.auth_repository.get_auth_by_id(id=auth_id)

        if not auth:
            logger.error(msg=f"Auth with id={auth_id} not exists.")
            raise UnauthorizedException(extra="Token is incorrect. Try again.")

        if str(auth.login_id) != login_id:
            logger.error(
                msg=f"Auth with id={auth_id} and login_id={login_id} not exists."
            )
            raise UnauthorizedException(extra="Token is incorrect. Try again.")

        auth.login_id = None

        auth.refresh_token_id = None

        auth = await self.auth_repository.update_auth(auth=auth)

        if not auth:
            logger.error(
                msg=f"Auth={auth} not updated when performing sign out operation."
            )
            raise ServerErrorException(extra="Auth not updated")

        return

    @staticmethod
    def _build_jwt_payload(
        auth_id: str,
        login_id: str,
        current_datetime: datetime,
        expires_delta: timedelta,
    ) -> JWTPayload:
        return JWTPayload(
            jti=str(uuid4()),
            auth_id=auth_id,
            login_id=login_id,
            iat=datetime_to_integer_timestamp(dt=current_datetime),
            exp=datetime_to_integer_timestamp(dt=current_datetime + expires_delta),
        )

    def _build_token(
        self,
        auth_id: str,
        login_id: str,
        current_datetime: datetime,
        expires_delta: timedelta,
    ) -> str:
        return self.jwt_auth.create_jwt_signed_with_rs256_algorithm(
            private_key_file_path=application_settings.private_key_file_path,
            jwt_payload=self._build_jwt_payload(
                auth_id=auth_id,
                login_id=login_id,
                current_datetime=current_datetime,
                expires_delta=expires_delta,
            ),
        )
