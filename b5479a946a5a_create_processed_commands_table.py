"""create_processed_commands_table

Revision ID: b5479a946a5a
Revises: 8a34c3f94b87
Create Date: ...

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "b5479a946a5a"
down_revision = "8a34c3f94b87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "processed_commands",
        sa.Column("key", UUID(as_uuid=True), nullable=False),
        sa.Column("actor_identity_user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("command_name", sa.String(length=64), nullable=False),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("result_room_id", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )


def downgrade() -> None:
    op.drop_table("processed_commands")
