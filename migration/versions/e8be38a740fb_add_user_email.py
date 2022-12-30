"""add user email

Revision ID: e8be38a740fb
Revises: a9de709ef721
Create Date: 2022-12-30 05:37:16.712098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8be38a740fb'
down_revision = 'a9de709ef721'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('email', sa.String(50), nullable=False,))


def downgrade() -> None:
    op.drop_column('user', 'email')
