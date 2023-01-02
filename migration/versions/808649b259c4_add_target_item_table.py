"""add target_item table

Revision ID: 808649b259c4
Revises: e8be38a740fb
Create Date: 2023-01-02 08:16:51.147577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '808649b259c4'
down_revision = 'e8be38a740fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'target_item',
        sa.Column('id', sa.Integer, nullable=False, index=True),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('keywords', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )



def downgrade() -> None:
    op.drop_table('target_item')
