"""add index on contributor and created_at for real_time_update

Revision ID: 5680194aac0b
Revises: 2762a0e3f0bf
Create Date: 2017-10-25 08:51:22.571752

"""

# revision identifiers, used by Alembic.
revision = "5680194aac0b"
down_revision = "2762a0e3f0bf"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index(
        "realtime_update_contributor_and_created_at",
        "real_time_update",
        ["created_at", "contributor"],
        unique=False,
    )


def downgrade():
    op.drop_index("realtime_update_contributor_and_created_at", table_name="real_time_update")
