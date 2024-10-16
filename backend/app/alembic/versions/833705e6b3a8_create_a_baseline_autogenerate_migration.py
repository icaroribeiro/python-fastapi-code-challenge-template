"""Create a baseline autogenerate migration

Revision ID: 833705e6b3a8
Revises: 
Create Date: 2024-01-01 19:05:50.659854

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "833705e6b3a8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("login_id", sa.UUID(), nullable=True),
        sa.Column("refresh_token_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("auth")
    # ### end Alembic commands ###
