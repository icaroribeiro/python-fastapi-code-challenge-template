import json

import jwt
import pytest
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from src.infrastructure.jwt.jwt_payload import JWTPayload


class TestJWTFixtures:
    @pytest.fixture
    def key(self) -> RsaKey:
        return RSA.generate(bits=4096)

    @pytest.fixture
    def private_key(self, key: RsaKey) -> bytes:
        return key.exportKey()

    @pytest.fixture
    def public_key(self, key: RsaKey) -> bytes:
        return key.public_key().exportKey()

    @pytest.fixture
    def private_key_file_path(self) -> str:
        return "./jwtRS256.key"

    @pytest.fixture
    def public_key_file_path(self) -> str:
        return "./jwtRS256.key.pub"

    @staticmethod
    def _build_token(jwt_payload: JWTPayload, private_key: bytes) -> str:
        return jwt.encode(
            payload=jwt_payload.dict(), key=private_key, algorithm="RS256"
        )
