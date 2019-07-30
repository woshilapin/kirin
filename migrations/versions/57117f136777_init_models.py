"""init of models

Revision ID: 57117f136777
Revises: None
Create Date: 2015-09-21 18:03:22.664662

"""

# revision identifiers, used by Alembic.
revision = "57117f136777"
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        "real_time_update",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("received_at", sa.DateTime(), nullable=False),
        sa.Column("contributor", sa.Text(), nullable=True),
        sa.Column("connector", sa.Enum("ire", "gtfs-rt", name="connector_type"), nullable=False),
        sa.Column("status", sa.Enum("OK", "KO", "pending", name="rt_status"), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("raw_data", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vehicle_journey",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("navitia_id", sa.Text(), nullable=False),
        sa.Column("circulation_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "navitia_id", "circulation_date", name="vehicle_journey_navitia_id_circulation_date_idx"
        ),
    )
    op.create_table(
        "trip_update",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("vj_id", postgresql.UUID(), nullable=False),
        sa.Column(
            "status", sa.Enum("add", "delete", "update", "none", name="modification_type"), nullable=False
        ),
        sa.ForeignKeyConstraint(["vj_id"], ["vehicle_journey.id"]),
        sa.PrimaryKeyConstraint("vj_id"),
    )
    op.create_table(
        "associate_realtimeupdate_tripupdate",
        sa.Column("real_time_update_id", postgresql.UUID(), nullable=False),
        sa.Column("trip_update_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["real_time_update_id"], ["real_time_update.id"]),
        sa.ForeignKeyConstraint(["trip_update_id"], ["trip_update.vj_id"]),
        sa.PrimaryKeyConstraint(
            "real_time_update_id", "trip_update_id", name="associate_realtimeupdate_tripupdate_pkey"
        ),
    )
    op.create_table(
        "stop_time_update",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("trip_update_id", postgresql.UUID(), nullable=False),
        sa.Column("stop_id", sa.Text(), nullable=False),
        sa.Column("departure", sa.DateTime(), nullable=True),
        sa.Column(
            "departure_status",
            sa.Enum("add", "delete", "update", "none", name="modification_type"),
            nullable=False,
        ),
        sa.Column("arrival", sa.DateTime(), nullable=True),
        sa.Column(
            "arrival_status",
            sa.Enum("add", "delete", "update", "none", name="modification_type"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["trip_update_id"], ["trip_update.vj_id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("stop_time_update")
    op.drop_table("associate_realtimeupdate_tripupdate")
    op.drop_table("trip_update")
    op.drop_table("vehicle_journey")
    op.drop_table("real_time_update")
    sa.Enum("", name="modification_type").drop(op.get_bind())
    sa.Enum("", name="connector_type").drop(op.get_bind())
    sa.Enum("", name="rt_status").drop(op.get_bind())
