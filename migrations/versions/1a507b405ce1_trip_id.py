"""using navitia trip id, not vj id

Revision ID: 1a507b405ce1
Revises: d5698d9b8bf
Create Date: 2015-10-14 11:33:29.646375

"""

# revision identifiers, used by Alembic.
revision = "1a507b405ce1"
down_revision = "d5698d9b8bf"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("vehicle_journey", "navitia_id", new_column_name="navitia_trip_id")
    op.create_unique_constraint(
        "vehicle_journey_navitia_trip_id_circulation_date_idx",
        "vehicle_journey",
        ["navitia_trip_id", "circulation_date"],
    )
    op.drop_constraint(u"vehicle_journey_navitia_id_circulation_date_idx", "vehicle_journey", type_="unique")


def downgrade():
    op.alter_column("vehicle_journey", "navitia_trip_id", new_column_name="navitia_id")
    op.create_unique_constraint(
        u"vehicle_journey_navitia_id_circulation_date_idx", "vehicle_journey", ["navitia_id", "circulation_date"]
    )
    op.drop_constraint("vehicle_journey_navitia_trip_id_circulation_date_idx", "vehicle_journey", type_="unique")
