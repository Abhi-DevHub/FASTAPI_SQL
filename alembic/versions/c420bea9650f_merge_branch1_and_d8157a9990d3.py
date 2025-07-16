"""merge branch1 and d8157a9990d3

Revision ID: c420bea9650f
Revises: branch1, d8157a9990d3
Create Date: 2025-07-14 13:23:56.788363

"""
from typing import Sequence, Union

from alembic import op # type: ignore
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c420bea9650f'
down_revision: Union[str, Sequence[str], None] = ('branch1', 'd8157a9990d3')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add 'first_name' and 'last_name' columns
    op.add_column('users', sa.Column('first_name', sa.String(length=56), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=56), nullable=True))
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)

    # copy the data from 'username' to 'first_name' and 'last_name'
   
    op.execute(
        """
        UPDATE users
        SET
            first_name = CASE
                WHEN POSITION(' ' IN username) > 0 THEN SUBSTRING(username FROM 1 FOR POSITION(' ' IN username) - 1)
                ELSE username
            END,
            last_name = CASE
                WHEN POSITION(' ' IN username) > 0 THEN SUBSTRING(username FROM POSITION(' ' IN username) + 1)
                ELSE NULL
            END
        WHERE username IS NOT NULL;
        """
    )

    # Remove 'username' column
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'username')


def downgrade() -> None:
    """Downgrade schema."""
    # Add 'username' column back first
    op.add_column('users', sa.Column('username', sa.String(length=56), nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

    # Combine first_name and last_name into username
    op.execute(
        """
        UPDATE users
        SET username =
            CASE
                WHEN last_name IS NOT NULL AND last_name <> '' THEN first_name || ' ' || last_name
                ELSE first_name
            END
        WHERE first_name IS NOT NULL;
        """
    )

    # Remove 'first_name' and 'last_name' columns
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    
