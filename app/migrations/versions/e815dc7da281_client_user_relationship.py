"""Client - User relationship

Revision ID: e815dc7da281
Revises: f623441a9cd1
Create Date: 2024-08-09 19:07:00.992602

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e815dc7da281"
down_revision: Union[str, None] = "f623441a9cd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
