from typing import List, Optional

from sqlalchemy import case, func, insert, select

from src.domain.model.salesperson_transaction_type import SalespersonTransactionType
from src.domain.model.transaction import (
    Transaction,
    TransactionBalanceBySalespersonType,
    TransactionType,
)


class TransactionRepository:
    def __init__(self, session):
        self.session = session

    async def create_transactions(
        self, transactions: List[Transaction]
    ) -> Optional[List[Transaction]]:
        async with self.session() as session:
            insert_statement = (
                insert(Transaction)
                .returning(Transaction)
                .values(
                    [
                        {
                            "type": transaction.type,
                            "date": transaction.date,
                            "product": transaction.product,
                            "value": transaction.value,
                            "salesperson": transaction.salesperson,
                            "file_id": transaction.file_id,
                        }
                        for transaction in transactions
                    ]
                )
            )

            result = await session.execute(statement=insert_statement)

            transactions = result.scalars()

            if not transactions:
                return None

            await session.commit()

            return transactions

    async def count_transactions(self) -> Optional[int]:
        async with self.session() as session:
            select_statement = select(func.count()).select_from(Transaction)

            result = await session.execute(statement=select_statement)

            count = result.scalar()

            if not count:
                return None

            return count

    async def read_transactions(
        self, offset: int, limit: int
    ) -> Optional[List[Transaction]]:
        async with self.session() as session:
            select_statement = select(Transaction)

            if offset:
                select_statement.offset(offset=offset)

            if limit:
                select_statement.limit(limit=limit)

            result = await session.execute(statement=select_statement)

            transactions = result.scalars()

            if not transactions:
                return None

            return transactions

    async def count_transaction_balances_by_salesperson_type(
        self, salesperson_type: int
    ) -> Optional[int]:
        async with self.session() as session:
            first_select_statement = (
                select(
                    TransactionType.type.label("transaction_type"),
                    TransactionType.sign.label("transaction_sign"),
                )
                .join(Transaction)
                .filter(
                    SalespersonTransactionType.transaction_type == TransactionType.type
                )
                .filter(SalespersonTransactionType.salesperson_type == salesperson_type)
                .subquery()
            )

            positive_balance = case(
                (first_select_statement.c.transaction_sign == "+", Transaction.value),
                else_=0,
            )

            negative_balance = case(
                (first_select_statement.c.transaction_sign == "-", -Transaction.value),
                else_=0,
            )

            second_select_statement = (
                (
                    Transaction.salesperson.label("salesperson"),
                    func.sum(positive_balance).label("positive_balance"),
                    func.sum(negative_balance).label("negative_balance"),
                    (func.sum(positive_balance) + func.sum(negative_balance)).label(
                        "total_balance"
                    ),
                )
                .join(first_select_statement)
                .filter(first_select_statement.c.transaction_type == Transaction.type)
                .group_by(Transaction.salesperson)
            )

            third_select_statement = select(func.count()).select_from(
                second_select_statement
            )

            result = await session.execute(statement=third_select_statement)

            count = result.scalar()

            if not count:
                return None

            return count

    async def read_transaction_balances_by_salesperson_type(
        self, salesperson_type: int, offset: int, limit: int
    ) -> Optional[List[TransactionBalanceBySalespersonType]]:
        async with self.session() as session:
            first_select_statement = (
                select(
                    TransactionType.type.label("transaction_type"),
                    TransactionType.sign.label("transaction_sign"),
                )
                .join(Transaction)
                .filter(
                    SalespersonTransactionType.transaction_type == TransactionType.type
                )
                .filter(SalespersonTransactionType.salesperson_type == salesperson_type)
                .subquery()
            )

            positive_balance = case(
                (first_select_statement.c.transaction_sign == "+", Transaction.value),
                else_=0,
            )

            negative_balance = case(
                (first_select_statement.c.transaction_sign == "-", -Transaction.value),
                else_=0,
            )

            second_select_statement = (
                (
                    Transaction.salesperson.label("salesperson"),
                    func.sum(positive_balance).label("positive_balance"),
                    func.sum(negative_balance).label("negative_balance"),
                    (func.sum(positive_balance) + func.sum(negative_balance)).label(
                        "total_balance"
                    ),
                )
                .join(first_select_statement)
                .filter(first_select_statement.c.transaction_type == Transaction.type)
                .group_by(Transaction.salesperson)
            )

            if offset:
                second_select_statement.offset(offset=offset)

            if limit:
                second_select_statement.limit(limit=limit)

            result = await session.execute(statement=second_select_statement)

            records = result.scalars()

            if not records:
                return None

            transaction_balances_by_salesperson_type = [
                TransactionBalanceBySalespersonType(
                    salersperson=record["salesperson"],
                    positive_balance=record["positive_balance"],
                    negative_balance=record["negative_balance"],
                    total_balance=record["total_balance"],
                )
                for record in records
            ]

            return transaction_balances_by_salesperson_type
