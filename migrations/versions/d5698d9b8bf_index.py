"""Index added

Revision ID: d5698d9b8bf
Revises: 57117f136777
Create Date: 2015-10-07 11:14:28.537210

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "d5698d9b8bf"
down_revision = "57117f136777"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index("vj_id_idx", "trip_update", ["vj_id"], unique=False)
    op.create_index("trip_update_id_idx", "stop_time_update", ["trip_update_id"], unique=False)
    op.create_index("contributor_idx", "real_time_update", ["contributor"], unique=False)


def downgrade():
    op.drop_index("contributor_idx", table_name="real_time_update")
    op.drop_index("trip_update_id_idx", table_name="stop_time_update")
    op.drop_index("vj_id_idx", table_name="trip_update")
