"""
Add cascade on foreign keys for downgrade

Revision ID: 396958f93bb
Revises: 396958f93ba
Create Date: 2018-09-11 14:26:11.238807

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "396958f93bb"
down_revision = "396958f93ba"

from alembic import op
import sqlalchemy as sa


def upgrade():
    # add cascade on foreign keys for a cleaner downgrade (when removing 'cots' real_time_updates)
    op.execute(
        "ALTER TABLE public.associate_realtimeupdate_tripupdate"
        "    DROP CONSTRAINT associate_realtimeupdate_tripupdate_real_time_update_id_fkey,"
        "    ADD CONSTRAINT associate_realtimeupdate_tripupdate_real_time_update_id_fkey"
        "        FOREIGN KEY (real_time_update_id) REFERENCES real_time_update(id) ON DELETE CASCADE"
    )
    op.execute(
        "ALTER TABLE public.associate_realtimeupdate_tripupdate"
        "    DROP CONSTRAINT associate_realtimeupdate_tripupdate_trip_update_id_fkey,"
        "    ADD CONSTRAINT associate_realtimeupdate_tripupdate_trip_update_id_fkey"
        "        FOREIGN KEY (trip_update_id) REFERENCES trip_update(vj_id) ON DELETE CASCADE"
    )
    op.execute(
        "ALTER TABLE public.trip_update"
        "    DROP CONSTRAINT trip_update_vj_id_fkey,"
        "    ADD CONSTRAINT trip_update_vj_id_fkey"
        "        FOREIGN KEY (vj_id) REFERENCES vehicle_journey(id) ON DELETE CASCADE"
    )
    op.execute(
        "ALTER TABLE public.stop_time_update"
        "    DROP CONSTRAINT stop_time_update_trip_update_id_fkey,"
        "    ADD CONSTRAINT stop_time_update_trip_update_id_fkey"
        "        FOREIGN KEY (trip_update_id) REFERENCES trip_update(vj_id) ON DELETE CASCADE"
    )


def downgrade():
    # remove vehicle_journey linked to a 'cots' realtime_update > will cascade on trip_update
    # trip_update will cascade on stop_time_update and associate_realtimeupdate_tripupdate
    # down revision manages 'cots' realtime_update removal
    op.execute(
        "DELETE FROM vehicle_journey WHERE id IN"
        "(SELECT trip_update_id FROM associate_realtimeupdate_tripupdate WHERE real_time_update_id IN"
        "(SELECT id FROM real_time_update WHERE connector='cots'))"
    )
    # back to no cascade
    op.execute(
        "ALTER TABLE public.associate_realtimeupdate_tripupdate"
        "    DROP CONSTRAINT associate_realtimeupdate_tripupdate_real_time_update_id_fkey,"
        "    ADD CONSTRAINT associate_realtimeupdate_tripupdate_real_time_update_id_fkey"
        "        FOREIGN KEY (real_time_update_id) REFERENCES real_time_update(id)"
    )
    op.execute(
        "ALTER TABLE public.associate_realtimeupdate_tripupdate"
        "    DROP CONSTRAINT associate_realtimeupdate_tripupdate_trip_update_id_fkey,"
        "    ADD CONSTRAINT associate_realtimeupdate_tripupdate_trip_update_id_fkey"
        "        FOREIGN KEY (trip_update_id) REFERENCES trip_update(vj_id)"
    )
    op.execute(
        "ALTER TABLE public.trip_update"
        "    DROP CONSTRAINT trip_update_vj_id_fkey,"
        "    ADD CONSTRAINT trip_update_vj_id_fkey"
        "        FOREIGN KEY (vj_id) REFERENCES vehicle_journey(id)"
    )
    op.execute(
        "ALTER TABLE public.stop_time_update"
        "    DROP CONSTRAINT stop_time_update_trip_update_id_fkey,"
        "    ADD CONSTRAINT stop_time_update_trip_update_id_fkey"
        "        FOREIGN KEY (trip_update_id) REFERENCES trip_update(vj_id)"
    )
