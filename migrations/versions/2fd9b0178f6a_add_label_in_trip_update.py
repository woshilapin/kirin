"""
Add label in trip_update
Revision ID: 2fd9b0178f6a
Revises: 51d98b3b8e58
Create Date: 2019-04-18 11:26:09.789277

"""

# revision identifiers, used by Alembic.
revision = '2fd9b0178f6a'
down_revision = '51d98b3b8e58'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('trip_update', sa.Column('label', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('trip_update', 'label')
