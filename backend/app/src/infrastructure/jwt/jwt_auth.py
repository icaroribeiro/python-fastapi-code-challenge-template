import jwt
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger

from src.infrastructure.jwt.jwt_payload import JWTPayload
from src.utils.api_exceptions import ServerErrorException


class JWTAuth:
    def __init__(self):
        pass

    @staticmethod
    def create_jwt_signed_with_rs256_algorithm(
        private_key_file_path: str, jwt_payload: JWTPayload
    ):
        try:
            with open(private_key_file_path, "rb") as f:
                private_key = f.read()
                token = jwt.encode(
                    payload=jsonable_encoder(jwt_payload),
                    key=private_key,
                    algorithm="RS256",
                )
        except Exception as ex:
            logger.error(
                msg=f"Failed to create jwt with payload={jwt_payload} and file={private_key_file_path}: ${str(ex)}"
            )
            raise ServerErrorException(extra="Token creation failed")

        return token

    @staticmethod
    def verify_jwt_signed_with_rs256_algorithm(
        public_key_file_path: str, token: str
    ) -> JWTPayload:
        try:
            with open(public_key_file_path, "rb") as f:
                public_key = f.read()
                jwt_payload = jwt.decode(
                    jwt=token, key=public_key, algorithms=["RS256"], leeway=1
                )
        except jwt.ExpiredSignatureError as ex:
            logger.error(
                msg=f"Signature of jwt={token} has expired for file={public_key_file_path}: {str(ex)}"
            )
            raise ServerErrorException(extra="Token signature has expired")
        except Exception as ex:
            logger.error(
                msg=f"Failed to verify jwt={token} with file={public_key_file_path}: ${str(ex)}"
            )
            raise ServerErrorException(extra="Token verification failed")

        return JWTPayload.parse_obj(obj=jwt_payload)
