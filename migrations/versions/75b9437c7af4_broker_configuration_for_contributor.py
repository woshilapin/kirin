"""broker configuration for contributor

Revision ID: 75b9437c7af4
Revises: 85a968ce3ce5
Create Date: 2020-09-30 09:11:27.861554

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "75b9437c7af4"
down_revision = "85a968ce3ce5"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("contributor", sa.Column("broker_url", sa.Text(), nullable=True))
    op.add_column("contributor", sa.Column("exchange_name", sa.Text(), nullable=True))
    op.add_column("contributor", sa.Column("queue_name", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("contributor", "broker_url")
    op.drop_column("contributor", "exchange_name")
    op.drop_column("contributor", "queue_name")
