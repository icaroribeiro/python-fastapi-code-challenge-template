from fastapi import status
from pydantic import BaseModel
from src.controller.model.error import Error


class UploadFileResponse(BaseModel):
    file_id: str
    uploaded_filename: str
    saved_filename: str


upload_file_responses = {
    status.HTTP_201_CREATED: {
        "model": UploadFileResponse,
        "description": "File successfully uploaded",
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
