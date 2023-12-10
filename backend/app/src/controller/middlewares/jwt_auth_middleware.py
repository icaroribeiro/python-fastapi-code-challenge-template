from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.logger import logger
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.application_container import AppContainer
from src.infrastructure import application_settings
from src.infrastructure.jwt.jwt_auth import JWTAuth
from src.utils.api_exceptions import ForbiddenException


class JWTAuthMiddleware(HTTPBearer):
    def __init__(
        self,
        auto_error: bool = True,
    ):
        super(JWTAuthMiddleware, self).__init__(auto_error=auto_error)

    @inject
    async def __call__(
        self,
        request: Request,
        jwt_auth: JWTAuth = Depends(Provide[AppContainer.infrastructure.jwt_auth]),
    ):
        try:
            token = await self._check_token(request=request)

            public_key_file_path = application_settings.public_key_file_path

            jwt_payload = jwt_auth.verify_jwt_signed_with_rs256_algorithm(
                public_key_file_path=public_key_file_path, token=token
            )

            request.state.auth_id = jwt_payload.auth_id

            request.state.login_id = jwt_payload.login_id
        except Exception:
            logger.error(
                f"Token verification failed in request to url={str(request.url)}"
            )
            raise

    async def _check_token(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTAuthMiddleware, self
        ).__call__(request)

        if not credentials:
            logger.warning("The authorization header wasn't present in the request")
            raise ForbiddenException(
                extra="The authorization header wasn't present in the request"
            )

        if not credentials.scheme == "Bearer":
            logger.error(
                "The authorization header of request didn't contain a bearer token"
            )
            raise ForbiddenException(
                extra="The authorization header of request didn't contain a bearer token"
            )

        return credentials.credentials
