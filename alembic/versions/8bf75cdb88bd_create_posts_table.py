"""create posts table

Revision ID: 8bf75cdb88bd
Revises:
Create Date: 2022-02-15 09:37:15.605977

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8bf75cdb88bd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
