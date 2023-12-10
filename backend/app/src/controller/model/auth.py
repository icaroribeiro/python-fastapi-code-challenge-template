from fastapi import status
from pydantic import BaseModel, Field
from src.controller.model.error import Error

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


class SignUpRequest(UserCreds):
    pass


class SignUpResponse(BaseModel):
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
