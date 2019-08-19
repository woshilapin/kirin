"""
Add company_id in trip_update
Revision ID: 4d9df787c7a7
Revises: 396958f93bb
Create Date: 2018-11-19 13:50:34.486383

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "4d9df787c7a7"
down_revision = "396958f93bb"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("trip_update", sa.Column("company_id", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("trip_update", "company_id")
