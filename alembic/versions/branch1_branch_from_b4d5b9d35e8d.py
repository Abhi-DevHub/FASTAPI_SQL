"""branch from b4d5b9d35e8d

Revision ID: branch1
Revises: b4d5b9d35e8d
Create Date: 2025-07-14 13:19:59.077581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'branch1'
down_revision: Union[str, Sequence[str], None] = 'b4d5b9d35e8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
