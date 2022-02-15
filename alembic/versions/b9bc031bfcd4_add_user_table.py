"""add user table

Revision ID: b9bc031bfcd4
Revises: 7d7e3530e7ea
Create Date: 2022-02-15 10:54:42.148531

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b9bc031bfcd4"
down_revision = "7d7e3530e7ea"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
