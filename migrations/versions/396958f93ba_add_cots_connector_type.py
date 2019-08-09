"""
Add 'cots' value to possible connector type

Revision ID: 396958f93ba
Revises: 575eb79e5a28
Create Date: 2018-08-24 14:26:11.238807

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "396958f93ba"
down_revision = "575eb79e5a28"

from alembic import op


def upgrade():
    # create new type, then switch type, finally remove old type
    op.execute("ALTER TYPE connector_type RENAME TO connector_type_tmp")
    op.execute("CREATE TYPE connector_type AS ENUM('ire', 'cots', 'gtfs-rt')")  # add 'cots' here
    op.execute(
        "ALTER TABLE real_time_update ALTER COLUMN connector TYPE connector_type USING connector::text::connector_type"
    )
    op.execute("DROP TYPE connector_type_tmp")


def downgrade():
    # first delete rows that are 'cots'
    op.execute("DELETE FROM real_time_update WHERE connector='cots'")

    op.execute("ALTER TYPE connector_type RENAME TO connector_type_tmp")
    op.execute("CREATE TYPE connector_type AS ENUM('ire', 'gtfs-rt')")  # no more 'cots'
    op.execute(
        "ALTER TABLE real_time_update ALTER COLUMN connector TYPE connector_type USING connector::text::connector_type"
    )
    op.execute("DROP TYPE connector_type_tmp")
