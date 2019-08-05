"""
adds start_timestamp to VJ without constraints

Revision ID: 2761a0e3f0bf
Revises: 37444da1fe56
Create Date: 2017-10-13 19:56:39.429947

"""

# revision identifiers, used by Alembic.
revision = "2761a0e3f0bf"
down_revision = "37444da1fe56"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("vehicle_journey", sa.Column("start_timestamp", sa.DateTime(), nullable=True))
    op.execute(
        "UPDATE vehicle_journey SET start_timestamp = circulation_date + TIME '00:00:00' "
        "WHERE start_timestamp IS NULL"
    )


def downgrade():
    op.drop_column("vehicle_journey", "start_timestamp")
