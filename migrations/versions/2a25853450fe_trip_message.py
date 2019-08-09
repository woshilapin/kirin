""" message added in trip_update

Revision ID: 2a25853450fe
Revises: 57117f136777
Create Date: 2015-10-08 17:21:33.744034

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "2a25853450fe"
down_revision = "1a507b405ce1"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("trip_update", sa.Column("message", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("trip_update", "message")
