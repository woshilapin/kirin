"""
Update attribut status with nullable=False and add an index status_idx

Revision ID: 3a12525235bf
Revises: 2763a0e3f0bf
Create Date: 2017-12-28 14:56:25.238546

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "3a12525235bf"
down_revision = "2763a0e3f0bf"

from alembic import op


def upgrade():
    op.execute("UPDATE real_time_update SET status = 'OK' WHERE status IS NULL")
    op.alter_column("real_time_update", "status", server_default="OK")
    op.create_index("status_idx", "real_time_update", ["status"], unique=False)


def downgrade():
    op.drop_index("status_idx", "real_time_update")
    op.alter_column("real_time_update", "status", nullable=True)
    op.execute("UPDATE real_time_update SET status = null WHERE status = 'OK'")
