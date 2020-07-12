"""empty message

Revision ID: 2d7686b59eee
Revises: 8c97251ca8b3
Create Date: 2020-07-10 17:03:13.191981

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2d7686b59eee'
down_revision = '8c97251ca8b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Show', sa.Column('w', sa.DateTime(), nullable=False))
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('Show', 'timestamp')
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    op.drop_column('Venue', 'web_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('web_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    op.add_column('Show', sa.Column('timestamp', postgresql.TIME(), autoincrement=False, nullable=True))
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('Show', 'w')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
