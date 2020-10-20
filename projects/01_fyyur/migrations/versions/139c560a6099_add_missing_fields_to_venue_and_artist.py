"""add missing fields to venue and artist

Revision ID: 139c560a6099
Revises: 2adc7282f276
Create Date: 2020-08-19 19:49:06.205557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "139c560a6099"
down_revision = "2adc7282f276"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "artist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=120), nullable=True),
        sa.Column("genres", sa.String(length=200), nullable=False),
        sa.Column("image_link", sa.String(length=500), nullable=True),
        sa.Column("facebook_link", sa.String(length=120), nullable=True),
        sa.Column("website", sa.String(length=120), nullable=True),
        sa.Column("seeking_venue", sa.Boolean(), nullable=True),
        sa.Column("seeking_description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "venue",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("genres", sa.String(length=120), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=120), nullable=True),
        sa.Column("image_link", sa.String(length=500), nullable=True),
        sa.Column("facebook_link", sa.String(length=120), nullable=True),
        sa.Column("website", sa.String(length=120), nullable=True),
        sa.Column("seeking_talent", sa.Boolean(), nullable=True),
        sa.Column("seeking_description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "show",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("artist_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["artist_id"], ["artist.id"],),
        sa.ForeignKeyConstraint(["venue_id"], ["venue.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "artists",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('artists_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column("city", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column("state", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column("phone", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column(
            "genres",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "facebook_link", sa.VARCHAR(length=500), autoincrement=False, nullable=True
        ),
        sa.Column("seeking_talent", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "seeking_description",
            sa.VARCHAR(length=500),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "image_link", sa.VARCHAR(length=500), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="artists_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "shows",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("venue_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("artist_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "start_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["artist_id"], ["artists.id"], name="shows_artist_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["venue_id"], ["venues.id"], name="shows_venue_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="shows_pkey"),
    )
    op.create_table(
        "venues",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("city", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column("state", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column(
            "address", sa.VARCHAR(length=120), autoincrement=False, nullable=True
        ),
        sa.Column("phone", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
        sa.Column(
            "image_link", sa.VARCHAR(length=500), autoincrement=False, nullable=True
        ),
        sa.Column(
            "facebook_link", sa.VARCHAR(length=120), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="venues_pkey"),
    )
    op.drop_table("show")
    op.drop_table("venue")
    op.drop_table("artist")
    # ### end Alembic commands ###
