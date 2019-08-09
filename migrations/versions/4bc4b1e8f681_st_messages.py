"""add message to stoptimeupdate

Revision ID: 4bc4b1e8f681
Revises: 196ca66cbcb
Create Date: 2015-12-03 11:07:05.551325

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "4bc4b1e8f681"
down_revision = "196ca66cbcb"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("stop_time_update", sa.Column("message", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("stop_time_update", "message")
