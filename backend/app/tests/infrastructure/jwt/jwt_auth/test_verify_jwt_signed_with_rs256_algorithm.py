from datetime import datetime, timedelta
from unittest.mock import mock_open, patch

import pytest
from fastapi import status
from src.infrastructure.jwt.jwt_auth import JWTAuth
from src.utils.api_exceptions import ServerErrorException
from src.utils.datetime import datetime_to_integer_timestamp
from tests.src.infrastructure.jwt.jwt_auth.test_jwt_auth_fixtures import (
    TestJWTAuthFixtures,
)
from tests.src.infrastructure.jwt.jwt_payload_factory import JWTPayloadFactory


class TestVerifyJWTSignedWithRS256Algorithm(TestJWTAuthFixtures):
    def test_should_verify_jwt_signed_with_rs256_algorithm(
        self,
        private_key: bytes,
        public_key: bytes,
        public_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        jwt_payload = JWTPayloadFactory()

        token = self._build_token(jwt_payload=jwt_payload, private_key=private_key)

        with patch("builtins.open", mock_open(read_data=public_key)) as mock_file:
            returned_jwt_payload = jwt_auth.verify_jwt_signed_with_rs256_algorithm(
                public_key_file_path=public_key_file_path,
                token=token,
            )

        assert returned_jwt_payload.__dict__ == jwt_payload.__dict__
        mock_file.asserefresh_token_called_with(public_key_file_path, "rb")

    def test_should_fail_with_500_when_file_cannot_be_open(
        self,
        public_key: bytes,
        public_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        token = ""

        with patch("builtins.open", mock_open(read_data=public_key)) as mock_file:
            mock_file.side_effect = Exception("failed")

            with pytest.raises(ServerErrorException) as ex:
                jwt_auth.verify_jwt_signed_with_rs256_algorithm(
                    public_key_file_path=public_key_file_path,
                    token=token,
                )
            assert str(ex.value.message) == "Oops! Something went wrong"
            assert str(ex.value.extra) == "Token verification failed"
            assert ex.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_file.asserefresh_token_called_with(public_key_file_path, "rb")

    def test_should_raises_exception_when_token_signature_has_expired(
        self,
        private_key: bytes,
        public_key: bytes,
        public_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        current_datetime = datetime.now()
        expires_delta = timedelta(minutes=-1)
        jwt_payload = JWTPayloadFactory(
            exp=datetime_to_integer_timestamp(dt=current_datetime + expires_delta)
        )

        token = self._build_token(jwt_payload=jwt_payload, private_key=private_key)

        with patch("builtins.open", mock_open(read_data=public_key)) as mock_file:
            with pytest.raises(ServerErrorException) as ex:
                jwt_auth.verify_jwt_signed_with_rs256_algorithm(
                    public_key_file_path=public_key_file_path,
                    token=token,
                )

            assert str(ex.value.message) == "Oops! Something went wrong"
            assert str(ex.value.extra) == "Token signature has expired"
            assert ex.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_file.asserefresh_token_called_with(public_key_file_path, "rb")

    def test_should_fail_with_500_when_key_date_is_not_in_correct_format(
        self,
        public_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        public_key = bytes("", "utf-8")
        token = ""

        with patch("builtins.open", mock_open(read_data=public_key)) as mock_file:
            with pytest.raises(ServerErrorException) as ex:
                jwt_auth.verify_jwt_signed_with_rs256_algorithm(
                    public_key_file_path=public_key_file_path,
                    token=token,
                )

            assert str(ex.value.message) == "Oops! Something went wrong"
            assert str(ex.value.extra) == "Token verification failed"
            assert ex.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_file.asserefresh_token_called_with(public_key_file_path, "rb")
