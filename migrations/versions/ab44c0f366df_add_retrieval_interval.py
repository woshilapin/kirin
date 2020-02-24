"""
Add a retrieval_interval to contributors

Revision ID: ab44c0f366df
Revises: 57860080e5d6
Create Date: 2020-02-12 16:56:35.678554

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "ab44c0f366df"
down_revision = "57860080e5d6"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "contributor", sa.Column("retrieval_interval", sa.Integer(), nullable=True, server_default="10")
    )


def downgrade():
    op.drop_column("contributor", "retrieval_interval")
