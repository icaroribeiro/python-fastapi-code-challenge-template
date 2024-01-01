import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class Default:
    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    created_at = Column(
        "created_at", DateTime(), nullable=False, default=datetime.utcnow()
    )
    updated_at = Column(
        "updated_at",
        DateTime(),
        nullable=True,
        default=None,
        onupdate=datetime.utcnow(),
    )
