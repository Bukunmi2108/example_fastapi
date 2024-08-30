"""Add content column

Revision ID: a896b3709e60
Revises: 493b0faf44b3
Create Date: 2024-08-29 22:00:22.105531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a896b3709e60'
down_revision: Union[str, None] = '493b0faf44b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
