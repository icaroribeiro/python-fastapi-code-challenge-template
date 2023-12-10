from unittest.mock import mock_open, patch

import pytest
from fastapi import status
from src.infrastructure.jwt.jwt_auth import JWTAuth
from src.utils.api_exceptions import ServerErrorException
from tests.src.infrastructure.jwt.jwt_auth.test_jwt_auth_fixtures import \
    TestJWTAuthFixtures
from tests.src.infrastructure.jwt.jwt_payload_factory import JWTPayloadFactory


class TestCreateJWTSignedWithRS256Algorithm(TestJWTAuthFixtures):
    def test_should_create_jwt_signed_with_rs256_algorithm(
        self,
        private_key: bytes,
        private_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        jwt_payload = JWTPayloadFactory()

        token = self._build_token(private_key=private_key, jwt_payload=jwt_payload)

        with patch("builtins.open", mock_open(read_data=private_key)) as mock_file:
            returned_token = jwt_auth.create_jwt_signed_with_rs256_algorithm(
                private_key_file_path=private_key_file_path,
                jwt_payload=jwt_payload,
            )

        assert returned_token == token
        mock_file.assert_called_with(private_key_file_path, "rb")

    def test_should_fail_with_500_when_file_cannot_be_open(
        self,
        private_key: bytes,
        private_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        jwt_payload = JWTPayloadFactory()

        with patch("builtins.open", mock_open(read_data=private_key)) as mock_file:
            mock_file.side_effect = Exception("failed")

            with pytest.raises(ServerErrorException) as ex:
                jwt_auth.create_jwt_signed_with_rs256_algorithm(
                    private_key_file_path=private_key_file_path, jwt_payload=jwt_payload
                )

            assert str(ex.value.message) == "Oops! Something went wrong"
            assert str(ex.value.extra) == "Token creation failed"
            assert ex.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_file.asserefresh_token_called_with(private_key_file_path, "rb")

    def test_should_fail_with_500_when_key_data_is_not_in_correct_format(
        self,
        private_key_file_path: str,
        jwt_auth: JWTAuth,
    ):
        private_key = bytes("", "utf-8")
        jwt_payload = JWTPayloadFactory()

        with patch("builtins.open", mock_open(read_data=private_key)) as mock_file:
            with pytest.raises(ServerErrorException) as ex:
                jwt_auth.create_jwt_signed_with_rs256_algorithm(
                    private_key_file_path=private_key_file_path,
                    jwt_payload=jwt_payload,
                )

            assert str(ex.value.message) == "Oops! Something went wrong"
            assert str(ex.value.extra) == "Token creation failed"
            assert ex.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_file.asserefresh_token_called_with(private_key_file_path, "rb")
