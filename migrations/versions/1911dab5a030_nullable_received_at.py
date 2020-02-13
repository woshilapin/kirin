"""
received_at is nullable (unused)

Revision ID: 1911dab5a030
Revises: ab44c0f366df
Create Date: 2020-02-26 18:37:18.275510

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "1911dab5a030"
down_revision = "ab44c0f366df"

from alembic import op


def upgrade():
    op.execute("ALTER TABLE real_time_update ALTER COLUMN received_at DROP NOT NULL;")


def downgrade():
    op.execute("UPDATE real_time_update SET received_at = created_at WHERE received_at IS NULL;")
    op.execute("ALTER TABLE real_time_update ALTER COLUMN received_at SET NOT NULL;")
