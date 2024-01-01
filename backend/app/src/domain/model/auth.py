from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin
from src.domain.model import Default
from src.infrastructure.database import Base


class Auth(Default, Base, SerializerMixin):
    __tablename__ = "auth"

    username = Column("username", String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    login_id = Column("login_id", UUID(as_uuid=True), nullable=True)
    refresh_token_id = Column("refresh_token_id", UUID(as_uuid=True), nullable=True)
