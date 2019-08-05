"""
Delete connector_type 'ire'
Revision ID: 4db0c66c3caf
Revises: 2fd9b0178f6a
Create Date: 2019-07-10 11:03:33.961995

"""

# revision identifiers, used by Alembic.
revision = "4db0c66c3caf"
down_revision = "2fd9b0178f6a"

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Delete from trip_update and related tables lines related to the connector 'ire'
    op.execute(
        "delete from trip_update where vj_id in ( \
               select trip_update_id from associate_realtimeupdate_tripupdate \
               inner join real_time_update on (real_time_update_id = real_time_update.id) \
               where connector = 'ire')"
    )

    # Delete lines in vehicle_journey without any use in trip_update
    op.execute("delete from vehicle_journey where id not in ( select vj_id from trip_update)")

    # Delete from real_time_update lines related to the connector 'ire'
    op.execute("DELETE FROM real_time_update WHERE connector='ire'")

    # delete type ire
    op.execute("ALTER TYPE connector_type RENAME TO connector_type_tmp")
    op.execute("CREATE TYPE connector_type AS ENUM('cots', 'gtfs-rt')")
    op.execute(
        "ALTER TABLE real_time_update ALTER COLUMN connector TYPE connector_type USING connector::text::connector_type"
    )
    op.execute("DROP TYPE connector_type_tmp")


def downgrade():
    # add type ire
    op.execute("ALTER TYPE connector_type RENAME TO connector_type_tmp")
    op.execute("CREATE TYPE connector_type AS ENUM('ire', 'cots', 'gtfs-rt')")
    op.execute(
        "ALTER TABLE real_time_update ALTER COLUMN connector TYPE connector_type USING connector::text::connector_type"
    )
    op.execute("DROP TYPE connector_type_tmp")
