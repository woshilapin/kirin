"""
removal of circulation_date (which is replaced by start_timestamp)
Follow up of migration 2762a0e3f0bf (done afterward so that the code/migrations are retrocompatible)

Revision ID: 2763a0e3f0bf
Revises: 5680194aac0b
Create Date: 2017-10-13 19:56:39.429947

"""

# revision identifiers, used by Alembic.
revision = '2763a0e3f0bf'
down_revision = '5680194aac0b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('vehicle_journey', 'circulation_date')


def downgrade():
    op.add_column(
        'vehicle_journey', sa.Column('circulation_date', sa.DATE(), autoincrement=False, nullable=True)
    )
    op.execute(
        "UPDATE vehicle_journey SET circulation_date = start_timestamp::date " "WHERE circulation_date IS NULL"
    )
