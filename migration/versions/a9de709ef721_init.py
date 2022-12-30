"""init

Revision ID: a9de709ef721
Revises: 
Create Date: 2022-12-29 23:37:15.949997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9de709ef721'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, nullable=False, index=True),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('age', sa.Integer),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('user')
