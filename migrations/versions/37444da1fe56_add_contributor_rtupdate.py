"""add contributor on realtime update

Revision ID: 37444da1fe56
Revises: 4bc4b1e8f681
Create Date: 2017-10-19 10:44:12.672505

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "37444da1fe56"
down_revision = "4bc4b1e8f681"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("real_time_update", sa.Column("contributor", sa.Text(), nullable=True))
    connection = op.get_bind()
    connection.execute(
        """UPDATE real_time_update
                          SET contributor = t.contributor
                          FROM trip_update t, associate_realtimeupdate_tripupdate art
                          WHERE t.vj_id = art.trip_update_id
                          AND real_time_update.id = art.real_time_update_id;"""
    )


def downgrade():
    op.drop_column("real_time_update", "contributor")
