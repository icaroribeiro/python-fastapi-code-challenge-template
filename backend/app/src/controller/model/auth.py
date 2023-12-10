from fastapi import status
from pydantic import BaseModel, Field

from src.controller.model.error import Error
from src.domain.model.token_schema import TokenSchema

USERNAME_REGEX = r"^[A-Za-z0-9]{7,14}$"

PASSWORD_REGEX = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

USERNAME_DESCRIPTION = (
    "It must have minimum 7 and maximum 15 characters in length. "
    "All characters can be alphabets or numbers."
)

PASSWORD_DESCRIPTION = (
    "It must have minimum 8 if characters in length. "
    "At least one uppercase letter. "
    "At least one lowercase letter. "
    "At least one digit. "
    "At least one special character."
)


class UserCreds(BaseModel):
    username: str = Field(regex=USERNAME_REGEX, description=USERNAME_DESCRIPTION)
    password: str = Field(regex=PASSWORD_REGEX, description=PASSWORD_DESCRIPTION)


class TokenResponse(TokenSchema):
    pass


class SignUpRequest(UserCreds):
    pass


class AuthResponse(BaseModel):
    username: str


class SignUpResponse(BaseModel):
    ok: bool


class LoginRequest(UserCreds):
    pass


class LoginResponse(TokenResponse):
    pass


class RefreshTokenRequest(BaseModel):
    token: str


class RefreshTokenResponse(TokenResponse):
    pass


class LogOutResponse(BaseModel):
    ok: bool


sign_up_responses = {
    status.HTTP_201_CREATED: {
        "model": SignUpResponse,
        "description": "Sign up successfully executed",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": Error,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": Error,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}

login_responses = {
    status.HTTP_200_OK: {
        "model": TokenResponse,
        "description": "Login successfully executed",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": Error,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": Error,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": Error,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}


refresh_token_responses = {
    status.HTTP_200_OK: {
        "model": TokenResponse,
        "description": "Token successfully refreshed",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": Error,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": Error,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": Error,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}


logout_responses = {
    status.HTTP_200_OK: {
        "model": LogOutResponse,
        "description": "Log out successfully executed",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": Error,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": Error,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}
