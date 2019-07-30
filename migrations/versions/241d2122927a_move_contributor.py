""" Move contributor

Revision ID: 241d2122927a
Revises: 2a25853450fe
Create Date: 2015-10-16 11:21:34.071037

"""

# revision identifiers, used by Alembic.
revision = '241d2122927a'
down_revision = '2a25853450fe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('trip_update', sa.Column('contributor', sa.Text(), nullable=True))

    connection = op.get_bind()
    result = connection.execute(
        'select rtu.contributor, '
        'art.trip_update_id '
        'from real_time_update rtu, associate_realtimeupdate_tripupdate art '
        'where rtu.id=art.real_time_update_id'
    )
    for row in result:
        if row['contributor'] and row['trip_update_id']:
            op.execute(
                "update trip_update set contributor='{}' where vj_id='{}'".format(
                    row['contributor'], row['trip_update_id']
                )
            )

    op.drop_index('contributor_idx', table_name='real_time_update')
    op.drop_column('real_time_update', 'contributor')
    op.create_index('contributor_idx', 'trip_update', ['contributor'], unique=False)
    op.create_index('circulation_date_idx', 'vehicle_journey', ['circulation_date'], unique=False)


def downgrade():
    op.add_column('real_time_update', sa.Column('contributor', sa.TEXT(), autoincrement=False, nullable=True))

    connection = op.get_bind()
    result = connection.execute(
        'select tu.contributor, art.real_time_update_id '
        'from trip_update tu, associate_realtimeupdate_tripupdate art '
        'where tu.vj_id=art.trip_update_id'
    )
    for row in result:
        if row['contributor'] and row['real_time_update_id']:
            op.execute(
                "update real_time_update set contributor='{}' where id='{}'".format(
                    row['contributor'], row['real_time_update_id']
                )
            )

    op.drop_index('contributor_idx', table_name='trip_update')
    op.drop_column('trip_update', 'contributor')
    op.drop_index('circulation_date_idx', table_name='vehicle_journey')
    op.create_index('contributor_idx', 'real_time_update', ['contributor'], unique=False)
