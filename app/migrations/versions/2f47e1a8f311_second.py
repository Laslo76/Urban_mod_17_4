"""second

Revision ID: 2f47e1a8f311
Revises: d888f371f227
Create Date: 2024-10-31 21:00:29.271906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f47e1a8f311'
down_revision: Union[str, None] = 'd888f371f227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
