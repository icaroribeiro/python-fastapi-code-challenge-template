import os
from datetime import datetime
from typing import Annotated, Union
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request, UploadFile, status
from fastapi.logger import logger

from src import AppContainer
from src.controller.model.pagination import (
    PAGE_NUMBER_DESCRIPTION,
    PAGE_SIZE_DESCRIPTION,
)
from src.controller.model.salesperson_type import SalespersonType
from src.controller.model.transaction import (
    PaginatedTransactionsResponse,
    paginated_transaction_balances_by_salesperson_type_responses,
    paginated_transactions_responses,
)
from src.controller.model.upload_file import UploadFileResponse, upload_file_responses
from src.infrastructure import application_settings
from src.service.transaction import TransactionService
from src.utils.api_exceptions import (
    BadRequestException,
    NoContentException,
    RequestEntityTooLargeException,
    ServerErrorException,
)
from src.utils.file_extension import is_allowed_file
from src.utils.pagination import build_next_page

transaction_tag = {
    "name": "transactions",
    "description": "Transaction related operations",
}

transaction_router = APIRouter(prefix="/transactions", tags=["transactions"])


@transaction_router.post(
    path="/upload-file",
    responses=upload_file_responses,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def upload_file(
    in_file: UploadFile,
    transaction_service: TransactionService = Depends(
        Provide[AppContainer.service.transaction_service]
    ),
):
    if not in_file:
        logger.warning(msg="No file sent")
        raise NoContentException()

    if in_file.filename == "":
        logger.warning(msg="No selected file")
        raise BadRequestException(extra="No selected file")

    if not is_allowed_file(filename=in_file.filename):
        logger.warning(msg=f"File extension of file={in_file.filename} not allowed")
        raise BadRequestException(
            extra=f"File extension of file={in_file.filename} not allowed"
        )

    file_size = len(await in_file.read())
    if file_size >= int(application_settings.max_transaction_file_content_size):
        logger.warning(msg=f"File={in_file.filename} is too large")
        raise RequestEntityTooLargeException(
            extra=f"File={in_file.filename} is too large"
        )

    await in_file.seek(0)

    file_id = str(uuid4())

    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

    filename = f"{current_time}_{file_id}_{in_file.filename}"

    in_file_path = os.path.join(application_settings.upload_folder, filename)

    try:
        with open(file=in_file_path, mode="wb") as out_file:
            while content := in_file.file.read(1024):
                out_file.write(content)

        await transaction_service.save_transactions(in_file_path=in_file_path)
    except Exception as ex:
        logger.error(f"Failed to upload the file={in_file.filename}: ${str(ex)}")
        if os.path.exists(in_file_path):
            os.remove(in_file_path)

        raise ServerErrorException(extra=f"File={in_file.filename} not stored")

    return UploadFileResponse(
        file_id=file_id, uploaded_filename=in_file.filename, saved_filename=filename
    )


@transaction_router.get(
    path="",
    responses=paginated_transactions_responses,
)
@inject
async def get_transactions(
    request: Request,
    page_number: Annotated[
        Union[int, None], Query(description=PAGE_NUMBER_DESCRIPTION)
    ] = 0,
    page_size: Annotated[
        Union[int, None], Query(description=PAGE_SIZE_DESCRIPTION)
    ] = 0,
    transaction_service: TransactionService = Depends(
        Provide[AppContainer.service.transaction_service]
    ),
):
    try:
        pagination = await transaction_service.list_transactions(
            page_number=page_number, page_size=page_size
        )
    except Exception as ex:
        logger.error(f"Failed to get transactions: ${str(ex)}")
        raise ServerErrorException(extra="Transaction not retrieved")

    print("url_path=", request.url.path)
    print("url_query=", request.url.query)
    print(
        "next_page=",
        build_next_page(
            url_path=request.url.path,
            url_query=request.url.query,
            next_page=pagination.next_page,
        ),
    )

    return PaginatedTransactionsResponse(
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        total_pages=pagination.total_pages,
        total_records=pagination.total_records,
        records=pagination.records,
        next_page="",
    )


@transaction_router.get(
    path="/balances",
    responses=paginated_transaction_balances_by_salesperson_type_responses,
)
@inject
async def get_transaction_balances_by_salesperson_type(
    request: Request,
    salesperson_type: Annotated[Union[SalespersonType, None], Query()] = "producer",
    page_number: Annotated[
        Union[int, None], Query(description=PAGE_NUMBER_DESCRIPTION)
    ] = 0,
    page_size: Annotated[
        Union[int, None], Query(description=PAGE_SIZE_DESCRIPTION)
    ] = 0,
    transaction_service: TransactionService = Depends(
        Provide[AppContainer.service.transaction_service]
    ),
):
    try:
        pagination = (
            await transaction_service.list_transaction_balances_by_salesperson_type(
                salesperson_type=salesperson_type.to_integer(),
                page_number=page_number,
                page_size=page_size,
            )
        )
    except Exception as ex:
        logger.error(
            f"Failed to get transaction balances by salesperson type: ${str(ex)}"
        )
        raise ServerErrorException(
            extra="Transaction balances by salesperson type not retrieved"
        )

    print("url_path=", request.url.path)
    print("url_query=", request.url.query)
    print(
        "next_page=",
        build_next_page(
            url_path=request.url.path,
            url_query=request.url.query,
            next_page=pagination.next_page,
        ),
    )

    return PaginatedTransactionsResponse(
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        total_pages=pagination.total_pages,
        total_records=pagination.total_records,
        records=pagination.records,
        next_page="",
    )
