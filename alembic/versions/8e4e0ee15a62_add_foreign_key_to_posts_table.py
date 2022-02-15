"""add foreign-key to posts table

Revision ID: 8e4e0ee15a62
Revises: b9bc031bfcd4
Create Date: 2022-02-15 11:11:46.165322

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8e4e0ee15a62"
down_revision = "b9bc031bfcd4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("post_users_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")
