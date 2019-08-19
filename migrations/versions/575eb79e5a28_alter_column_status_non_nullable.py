"""
Alter attibut status with nullable = False

Revision ID: 575eb79e5a28
Revises: 3a12525235bf
Create Date: 2018-02-06 17:54:25.421283

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "575eb79e5a28"
down_revision = "3a12525235bf"

from alembic import op


def upgrade():
    op.execute("UPDATE real_time_update SET status = 'OK' WHERE status IS NULL")
    op.alter_column("real_time_update", "status", nullable=False)


def downgrade():
    op.alter_column("real_time_update", "status", nullable=True)
