"""remove all stoptimes

Revision ID: 196ca66cbcb
Revises: 49feac4289a4
Create Date: 2015-11-30 15:18:15.104863

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "196ca66cbcb"
down_revision = "49feac4289a4"

from alembic import op


def upgrade():
    """
    before all times were from local navitia time and we want only UTC.

    since all stoptimes are thus false, we remove all of them
    """
    op.execute("""TRUNCATE TABLE stop_time_update;""")
    op.execute(
        """DELETE from associate_realtimeupdate_tripupdate WHERE \
              trip_update_id in (select vj_id from trip_update WHERE status != 'delete');"""
    )
    op.execute("""DELETE from trip_update WHERE status != 'delete';""")
    op.execute("""DELETE from vehicle_journey WHERE id not in (select vj_id from trip_update);""")


def downgrade():
    # no way to get the old stoptimes back :p
    pass
