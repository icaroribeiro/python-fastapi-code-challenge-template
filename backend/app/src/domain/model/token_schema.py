from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    token_type: str = "Bearer"
