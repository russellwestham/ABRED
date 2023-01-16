"""created construction table and api

Revision ID: 9f8bec50fc0b
Revises: 808649b259c4
Create Date: 2023-01-10 16:21:44.050049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f8bec50fc0b'
down_revision = '808649b259c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'News',
        sa.Column('id', sa.Integer, nullable=False, index=True),
        sa.Column('const_id', sa.Integer, nullable=False, index=True),
        sa.Column('thumnl_url', sa.String(length=50), nullable=False),
        sa.Column('url', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['const_id'], ['Construction.id'], )

    )


def downgrade() -> None:
    op.drop_table('Construction')
