import re

from fastapi import status
from pydantic import BaseModel, Field, field_validator
from src.controller.dto.error_dto import ErrorDto

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


class UserCredsDto(BaseModel):
    username: str = Field(description=USERNAME_DESCRIPTION)
    password: str = Field(description=PASSWORD_DESCRIPTION)

    @field_validator("username")
    @classmethod
    def username_regex_match(cls, username: str) -> str:
        regex_for_username: re.Pattern[str] = re.compile(USERNAME_REGEX)
        if not regex_for_username.match(username):
            raise ValueError("invalid username")
        return username

    @field_validator("password")
    @classmethod
    def password_regex_match(cls, password: str) -> str:
        regex_for_password: re.Pattern[str] = re.compile(PASSWORD_REGEX)
        if not regex_for_password.match(password):
            raise ValueError("invalid password")
        return password


class SignUpRequestDto(UserCredsDto):
    pass


class SignUpResponseDto(BaseModel):
    ok: bool


sign_up_responses = {
    status.HTTP_201_CREATED: {
        "model": SignUpResponseDto,
        "description": "Sign up successfully executed",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorDto,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ErrorDto,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorDto,
    },
}
