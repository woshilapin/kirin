"""add delay on stop times departure and arrival

Revision ID: d6469f134d7
Revises: 241d2122927a
Create Date: 2015-10-23 12:11:20.702334

"""

# revision identifiers, used by Alembic.
revision = "d6469f134d7"
down_revision = "241d2122927a"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("stop_time_update", sa.Column("arrival_delay", sa.Interval(), nullable=True))
    op.add_column("stop_time_update", sa.Column("departure_delay", sa.Interval(), nullable=True))


def downgrade():
    op.drop_column("stop_time_update", "departure_delay")
    op.drop_column("stop_time_update", "arrival_delay")
