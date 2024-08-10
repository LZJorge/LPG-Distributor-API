"""Add clients table

Revision ID: f623441a9cd1
Revises: d5e112383b02
Create Date: 2024-07-04 20:19:05.787008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f623441a9cd1'
down_revision: Union[str, None] = 'd5e112383b02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
