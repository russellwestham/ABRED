"""creation construction table and news table again

Revision ID: 3d2eb37bfcf4
Revises: 7b12567837d2
Create Date: 2023-01-17 08:12:15.268781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d2eb37bfcf4'
down_revision = '7b12567837d2'
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
        sa.Column('keywords', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
    'News',
        sa.Column('id', sa.Integer, nullable=False, index=True),
        sa.Column('construction_id', sa.Integer, nullable=False, index=True),
        sa.Column('thumnl_url', sa.String(length=100), nullable=False),
        sa.Column('url', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=False),
        # sa.Column('keywords', sa.String(length=100), nullable=False),
        sa.Column('ks_graph', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['construction_id'], ['Construction.id'])
    )


def downgrade() -> None:
    op.drop_table('News')
    op.drop_table('Construction')
