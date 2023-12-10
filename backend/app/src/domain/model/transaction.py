import enum

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from src.domain.model import Default
from src.infrastructure.database import Base


class SourceItem(enum.Enum):
    Enter = "Entrada"
    Exit = "Saída"


class SignItem(enum.Enum):
    Plus = "+"
    Minus = "-"


class TransactionType(Default, Base):
    __tablename__ = "transaction_type"

    type = Column("type", Integer, nullable=False)
    description = Column("description", String, nullable=False)
    source = Column("source", Enum(SourceItem), nullable=False)
    sign = Column("sign", Enum(SignItem), nullable=False)


class Transaction(Default, Base, SerializerMixin):
    __tablename__ = "transaction"

    type = Column("type", Integer, ForeignKey(TransactionType.type), nullable=False)
    date = Column("date", DateTime(), nullable=False)
    product = Column("product", String, nullable=False)
    value = Column("value", Float, nullable=False)
    salesperson = Column("salesperson", String, nullable=False)
    file_id = Column("file_id", UUID(as_uuid=True), nullable=False)


class TransactionBalanceBySalespersonType(BaseModel):
    salesperson: str
    positive_balance: float
    negative_balance: float
    total_balance: float
