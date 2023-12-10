from datetime import datetime
from typing import List

from fastapi import status
from pydantic import BaseModel

from src.controller.model.error import Error
from src.controller.model.pagination import BasePaginationResponse
from src.controller.model.salesperson_type import SalespersonType


class TransactionResponse(BaseModel):
    id: str
    type: int
    date: datetime
    product: str
    value: float
    salesperson: str
    file_id: str


class PaginatedTransactionsResponse(BasePaginationResponse):
    records: List[TransactionResponse]


class TransactionBalancesBySalespersonTypeResponse(BaseModel):
    salesperson: str
    salesperson_type: SalespersonType
    positive_balance: float
    negative_balance: float
    final_balance: float


class PaginatedTransactionBalancesBySalespersonTypeResponse(BasePaginationResponse):
    records: List[TransactionBalancesBySalespersonTypeResponse]


paginated_transactions_responses = {
    status.HTTP_200_OK: {
        "model": PaginatedTransactionsResponse,
        "description": "Transactions successfully retrieved",
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": Error,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}


paginated_transaction_balances_by_salesperson_type_responses = {
    status.HTTP_200_OK: {
        "model": PaginatedTransactionBalancesBySalespersonTypeResponse,
        "description": "Transaction balances by salesperson type successfully retrieved",
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": Error,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": Error,
    },
}
