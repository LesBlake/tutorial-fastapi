"""add content column to post table

Revision ID: 7d7e3530e7ea
Revises: 8bf75cdb88bd
Create Date: 2022-02-15 10:49:47.601760

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7d7e3530e7ea"
down_revision = "8bf75cdb88bd"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade():
    op.drop_column("posts", "content")
