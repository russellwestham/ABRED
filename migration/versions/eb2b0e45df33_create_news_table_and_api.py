"""create news table and api

Revision ID: eb2b0e45df33
Revises: 9f8bec50fc0b
Create Date: 2023-01-10 12:21:36.566833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb2b0e45df33'
down_revision = '9f8bec50fc0b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Construction',
        sa.Column('id', sa.Integer, nullable=False, index=True),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('stage', sa.String(length=50), nullable=False),
        sa.Column('address', sa.String(length=50), nullable=False),
        sa.Column('gis_data', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('Construction')