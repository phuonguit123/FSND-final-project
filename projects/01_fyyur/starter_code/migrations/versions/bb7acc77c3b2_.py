"""empty message

Revision ID: bb7acc77c3b2
Revises: 16fb17e09555
Create Date: 2020-04-08 01:06:18.939955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bb7acc77c3b2'
down_revision = '16fb17e09555'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.alter_column('Artist', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)
    op.add_column('Show', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.create_unique_constraint('artist_avail', 'Show', ['artist_id', 'start_time'])
    op.create_unique_constraint('venue_avail', 'Show', ['venue_id', 'start_time'])
    op.add_column('Venue', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'created_at')
    op.drop_constraint('venue_avail', 'Show', type_='unique')
    op.drop_constraint('artist_avail', 'Show', type_='unique')
    op.drop_column('Show', 'created_at')
    op.alter_column('Artist', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)
    op.drop_column('Artist', 'created_at')
    # ### end Alembic commands ###
