"""
Add attribut effect in trip_update
Revision ID: 45f4c90aa775
Revises: 4d9df787c7a7
Create Date: 2018-11-23 09:55:16.326118

"""

# revision identifiers, used by Alembic.
revision = '45f4c90aa775'
down_revision = '4d9df787c7a7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

trip_effect = sa.Enum(
    'NO_SERVICE',
    'REDUCED_SERVICE',
    'SIGNIFICANT_DELAYS',
    'DETOUR',
    'ADDITIONAL_SERVICE',
    'MODIFIED_SERVICE',
    'OTHER_EFFECT',
    'UNKNOWN_EFFECT',
    'STOP_MOVED',
    name='trip_effect',
)


def upgrade():
    trip_effect.create(op.get_bind(), checkfirst=True)
    op.add_column('trip_update', sa.Column('effect', trip_effect, nullable=True))


def downgrade():
    op.drop_column('trip_update', 'effect')
    sa.Enum('', name='trip_effect').drop(op.get_bind(), checkfirst=True)
