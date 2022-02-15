"""add more Cols to Posts

Revision ID: 21358004b49e
Revises: 8e4e0ee15a62
Create Date: 2022-02-15 11:21:25.673505

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "21358004b49e"
down_revision = "8e4e0ee15a62"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column(
            "published", sa.Boolean(), server_default=sa.text("TRUE"), nullable=False
        ),
    ),
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
