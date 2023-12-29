from controller.dto.error_response_dto import ErrorResponseDto
from src.controller.dto.user_credentials_dto import UserCredentialsDto


class SignUpResponseDto(UserCredentialsDto):
    pass


sign_up_responses = {
    status.HTTP_201_CREATED: {
        "model": SignUpResponseDto,
        "description": "Sign up successfully executed",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponseDto,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ErrorResponseDto,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorResponseDto,
    },
}
