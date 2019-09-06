"""
Add attribut is_active in contributor
Revision ID: 21194e8e2308
Revises: 443587af1780
Create Date: 2019-09-06 14:56:15.912974

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = '21194e8e2308'
down_revision = u'443587af1780'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add column is_active in contributor
    op.add_column('contributor', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    # Drop column is_visible
    op.drop_column('contributor', 'is_active')
