from datetime import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, status
from fastapi.logger import logger

from src.application_container import AppContainer
from src.controller.middlewares.jwt_auth_middleware import JWTAuthMiddleware
from src.controller.model.auth import (
    AuthResponse,
    LoginRequest,
    LogOutResponse,
    RefreshTokenRequest,
    SignUpRequest,
    SignUpResponse,
    TokenResponse,
    login_responses,
    logout_responses,
    refresh_token_responses,
    sign_up_responses,
)
from src.domain.model.auth import Auth
from src.service.auth import AuthService
from src.utils.api_exceptions import (
    ApiException,
    ServerErrorException,
    UnauthorizedException,
)
from src.utils.security import get_hashed_password

auth_tag = {
    "name": "auth",
    "description": "Authentication related operations",
}

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/sign-up", responses=sign_up_responses, status_code=status.HTTP_201_CREATED
)
@inject
async def sign_up(
    sign_up_request: SignUpRequest,
    auth_service: AuthService = Depends(Provide[AppContainer.service.auth_service]),
):
    try:
        auth = Auth()
        auth.username = sign_up_request.username
        auth.password = get_hashed_password(password=sign_up_request.password)
        created_auth = await auth_service.save_auth(auth=auth)
    except Exception as ex:
        logger.error(f"Failed to sign up: ${str(ex)}")
        raise ServerErrorException(extra="Sign up failed")

    return AuthResponse()


@auth_router.post(
    path="/login", responses=login_responses, status_code=status.HTTP_200_OK
)
@inject
async def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(Provide[AppContainer.service.auth_service]),
):
    try:
        current_datetime = datetime.now()

        username = login_request.username

        password = login_request.password

        token_schema = await auth_service.sign_in(
            username=username, password=password, current_datetime=current_datetime
        )
    except UnauthorizedException:
        raise
    except Exception as ex:
        logger.error(f"Failed to execute log in operation : ${str(ex)}")
        raise ServerErrorException(extra="Log in failed")

    return TokenResponse.parse_obj(obj=token_schema)


@auth_router.post(
    path="/refresh-token",
    responses=refresh_token_responses,
    status_code=status.HTTP_200_OK,
)
@inject
async def refresh_token(
    refresh_token_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(Provide[AppContainer.service.auth_service]),
):
    try:
        current_datetime = datetime.now()

        token = refresh_token_request.token

        token_schema = await auth_service.renew_token(
            token=token,
            current_datetime=current_datetime,
        )
    except UnauthorizedException:
        raise
    except Exception as ex:
        logger.error(f"Failed to execute refresh token operation: ${str(ex)}")
        raise ServerErrorException(extra="Refresh token failed")

    return TokenResponse.parse_obj(obj=token_schema)


@auth_router.post(
    path="/logout",
    responses=logout_responses,
    dependencies=[Depends(JWTAuthMiddleware())],
)
@inject
async def logout(
    request: Request,
    auth_service: AuthService = Depends(Provide[AppContainer.service.auth_service]),
):
    try:
        auth_id = request.state.auth_id

        login_id = request.state.login_id

        await auth_service.sign_out(auth_id=auth_id, login_id=login_id)
    except ApiException as ex:
        logger.error(f"Failed to execute log out operation: ${str(ex.extra)}")
        raise
    except Exception as ex:
        logger.error(f"Failed to execute log out operation: ${str(ex)}")
        raise

    return LogOutResponse(ok=True)
