from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.logger import logger
from src.application_container import AppContainer
from src.router.dto.sign_up_request_dto import SignUpRequestDto
from src.router.dto.sign_up_response_dto import SignUpResponseDto, sign_up_responses
from src.domain.model.auth import Auth
from src.service.auth_service import AuthService
from src.utils.api_exceptions import ServerErrorException
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
    sign_up_request: SignUpRequestDto,
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

    return SignUpResponseDto(ok=True)
