"""add index on field created_at for realtime_updates

Revision ID: 49feac4289a4
Revises: 51d2d334dd4f
Create Date: 2015-11-03 12:18:31.935198

"""

# revision identifiers, used by Alembic.
revision = "49feac4289a4"
down_revision = "51d2d334dd4f"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index("realtime_update_created_at", "real_time_update", ["created_at"], unique=False)


def downgrade():
    op.drop_index("realtime_update_created_at", table_name="real_time_update")
