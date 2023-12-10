from sqlalchemy import Column, ForeignKey, Integer

from src.domain.model import Default
from src.domain.model.transaction import TransactionType
from src.infrastructure.database import Base


class SalespersonTransactionType(Default, Base):
    __tablename__ = "salesperson_transaction_type"

    salesperson_type = Column("salesperson_type", Integer, nullable=False)
    transaction_type = Column(
        "transaction_type", Integer, ForeignKey(TransactionType.type), nullable=False
    )
