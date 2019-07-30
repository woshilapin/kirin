"""
adds constraint to start_timestamp to VJ (will replace circulation_date)
rm of circulation_date (2763a0e3f0bf) is done in another PR to allow retrocompatible code/migrations

Revision ID: 2762a0e3f0bf
Revises: 2761a0e3f0bf
Create Date: 2017-10-13 19:57:39.429947

"""

# revision identifiers, used by Alembic.
revision = '2762a0e3f0bf'
down_revision = '2761a0e3f0bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # needs to be done again in case some were created during previous upgrade
    op.execute(
        "UPDATE vehicle_journey SET start_timestamp=circulation_date + TIME '00:00:00' "
        "WHERE start_timestamp IS NULL"
    )
    # add constraints on start_timestamp
    op.alter_column('vehicle_journey', 'start_timestamp', nullable=False)
    op.create_unique_constraint(
        'vehicle_journey_navitia_trip_id_start_timestamp_idx',
        'vehicle_journey',
        ['navitia_trip_id', 'start_timestamp'],
    )
    op.create_index('start_timestamp_idx', 'vehicle_journey', ['start_timestamp'], unique=False)

    # remove all the constraints on circulation_date
    op.drop_index('circulation_date_idx', table_name='vehicle_journey')
    op.drop_constraint(
        u'vehicle_journey_navitia_trip_id_circulation_date_idx', 'vehicle_journey', type_='unique'
    )
    op.alter_column('vehicle_journey', 'circulation_date', nullable=True)


def downgrade():
    # needs to be done "again"(reverse as we downgrade) in case some were created during previous downgrade
    op.execute(
        "UPDATE vehicle_journey SET circulation_date = start_timestamp::date " "WHERE circulation_date IS NULL"
    )
    # add all the constraints on circulation_date
    op.alter_column('vehicle_journey', 'circulation_date', nullable=False)
    op.create_unique_constraint(
        u'vehicle_journey_navitia_trip_id_circulation_date_idx',
        'vehicle_journey',
        ['navitia_trip_id', 'circulation_date'],
    )
    op.create_index('circulation_date_idx', 'vehicle_journey', ['circulation_date'], unique=False)

    # remove constraints on start_timestamp
    op.drop_index('start_timestamp_idx', table_name='vehicle_journey')
    op.drop_constraint('vehicle_journey_navitia_trip_id_start_timestamp_idx', 'vehicle_journey', type_='unique')
    op.alter_column('vehicle_journey', 'start_timestamp', nullable=True)
