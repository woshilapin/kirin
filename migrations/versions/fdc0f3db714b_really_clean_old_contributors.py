"""
REALLY delete column contributor from tables real_time_update and trip_update

This migration was in 57860080e5d6, but it was too soon (see comments in migration).
As it was applied already for some platforms, removal is conditional (IF EXISTS).

Revision ID: fdc0f3db714b
Revises: ab44c0f366df
Create Date: 2020-02-25 14:12:48.880949

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "fdc0f3db714b"
down_revision = "ab44c0f366df"

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Conditionally drop indexes on contributor
    op.execute("DROP INDEX IF EXISTS realtime_update_contributor_and_created_at;")
    op.execute("DROP INDEX IF EXISTS contributor_idx;")

    # Conditionally drop column contributor
    op.execute("ALTER TABLE real_time_update DROP COLUMN IF EXISTS contributor;")
    op.execute("ALTER TABLE trip_update DROP COLUMN IF EXISTS contributor;")


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
