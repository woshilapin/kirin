"""
Empty migration // Used to be:
Deleting column contributor from tables real_time_update and trip_update

Not anymore, as these removals should only be done when no version in prod is using concerned fields.
And db migration is applied before deploying Kirin itself.
So version n-1 should not use fields, no more than version n.

But it is still used in 3.0.0 and only unused from 4.0.0.
So no removal can be done in 4.0.x (and columns are actually unused)
The actual db removal will be done in a version >= 4.1.0

Revision ID: 57860080e5d6
Revises: 21194e8e2308
Create Date: 2019-09-05 17:16:35.675541

"""
from __future__ import absolute_import, print_function, unicode_literals, division

# revision identifiers, used by Alembic.
revision = "57860080e5d6"
down_revision = "21194e8e2308"


def upgrade():
    # To be done in a later revision
    pass


def downgrade():
    # To be done in a later revision
    pass
