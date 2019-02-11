"""empty message
Add physical_mode_id in trip_update
Revision ID: 51d98b3b8e58
Revises: 174583a01aea
Create Date: 2019-02-11 16:28:16.999441

"""

# revision identifiers, used by Alembic.
revision = '51d98b3b8e58'
down_revision = '174583a01aea'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('trip_update', sa.Column('physical_mode_id', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('trip_update', 'physical_mode_id')
