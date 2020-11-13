"""add contributor

Revision ID: 53647ffeb3c6
Revises: 4db0c66c3caf
Create Date: 2019-08-13 12:36:25.829578

"""

from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "53647ffeb3c6"
down_revision = "4db0c66c3caf"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from kirin.core import model


def upgrade():
    op.create_table(
        "contributor",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("navitia_coverage", sa.Text(), nullable=False),
        sa.Column("navitia_token", sa.Text(), nullable=True),
        sa.Column("feed_url", sa.Text(), nullable=True),
        sa.Column(
            "connector_type",
            sa.Enum("cots", "gtfs-rt", name="connector_type", metadata=model.meta),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("contributor")
