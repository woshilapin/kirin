"""
Deleting column contributor from tables real_time_update and trip_update
Revision ID: 57860080e5d6
Revises: 443587af1780
Create Date: 2019-09-05 17:16:35.675541

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "57860080e5d6"
down_revision = "443587af1780"

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Drop indexes on contributor
    op.drop_index("realtime_update_contributor_and_created_at", table_name="real_time_update")
    op.drop_index("contributor_idx", table_name="trip_update")

    # Drop column contributor
    op.drop_column("real_time_update", "contributor")
    op.drop_column("trip_update", "contributor")


def downgrade():
    # Add column contributor in the tables real_time_update and trip_update
    op.add_column("trip_update", sa.Column("contributor", sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column("real_time_update", sa.Column("contributor", sa.TEXT(), autoincrement=False, nullable=True))

    # Add indexes on contributor
    op.create_index("contributor_idx", "trip_update", ["contributor"], unique=False)
    op.create_index(
        "realtime_update_contributor_and_created_at",
        "real_time_update",
        ["created_at", "contributor"],
        unique=False,
    )

    # Update contributor with the value of contributor_id
    op.execute("UPDATE real_time_update SET contributor = contributor_id;")
    op.execute("UPDATE trip_update SET contributor = contributor_id;")
