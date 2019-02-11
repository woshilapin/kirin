"""empty message

Revision ID: 174583a01aea
Revises: 45f4c90aa775
Create Date: 2018-11-28 14:58:50.362398

"""

# revision identifiers, used by Alembic.
revision = '174583a01aea'
down_revision = '45f4c90aa775'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.execute("COMMIT")
    op.execute("ALTER type modification_type ADD VALUE 'deleted_for_detour'")
    op.execute("ALTER type modification_type ADD VALUE 'added_for_detour'")

def downgrade():
    op.execute("ALTER TABLE stop_time_update ALTER COLUMN departure_status TYPE text")
    op.execute("ALTER TABLE stop_time_update ALTER COLUMN arrival_status TYPE text")
    op.execute("ALTER TABLE trip_update ALTER COLUMN status TYPE text")

    op.execute("UPDATE stop_time_update SET arrival_status='add' WHERE arrival_status='added_for_detour'")
    op.execute("UPDATE stop_time_update SET arrival_status='delete' WHERE arrival_status='deleted_for_detour'")

    op.execute("UPDATE stop_time_update SET departure_status='add' WHERE departure_status='added_for_detour'")
    op.execute("UPDATE stop_time_update SET departure_status='delete' WHERE departure_status='deleted_for_detour'")

    op.execute("UPDATE trip_update SET status='add' WHERE status='added_for_detour'")
    op.execute("UPDATE trip_update SET status='delete' WHERE status='deleted_for_detour'")

    sa.Enum('', name='modification_type').drop(op.get_bind())

    op.execute("CREATE TYPE modification_type AS ENUM ('add', 'delete', 'update', 'none')")

    op.execute("ALTER TABLE stop_time_update ALTER COLUMN departure_status TYPE modification_type USING departure_status::modification_type")
    op.execute("ALTER TABLE stop_time_update ALTER COLUMN arrival_status TYPE modification_type USING arrival_status::modification_type")
    op.execute("ALTER TABLE trip_update ALTER COLUMN status TYPE modification_type USING status::modification_type")


