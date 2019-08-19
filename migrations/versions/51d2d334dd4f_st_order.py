""" Add an order to the stoptime in order to sort the stoptimes in the TripUpdate

Revision ID: 51d2d334dd4f
Revises: d6469f134d7
Create Date: 2015-10-23 17:04:11.216638

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "51d2d334dd4f"
down_revision = "d6469f134d7"

from alembic import op
import sqlalchemy as sa


def upgrade():
    """
    The migration is a bit complex because without order, we cannot use the stoptimes list in the db
    so we remove all stop times in the db before (at the moment of the migration only trip cancellation are
    handled thus the stoptimes are not important)
    """
    op.execute("""TRUNCATE TABLE stop_time_update;""")
    op.execute(
        """DELETE from associate_realtimeupdate_tripupdate WHERE \
              trip_update_id in (select vj_id from trip_update WHERE status != 'delete');"""
    )
    op.execute("""DELETE from trip_update WHERE status != 'delete';""")
    op.execute("""DELETE from vehicle_journey WHERE id not in (select vj_id from trip_update);""")

    op.add_column("stop_time_update", sa.Column("order", sa.Integer(), nullable=False))


def downgrade():
    op.drop_column("stop_time_update", "order")
