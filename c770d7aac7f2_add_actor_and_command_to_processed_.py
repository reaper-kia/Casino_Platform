"""add_actor_and_command_to_processed_commands

Revision ID: c770d7aac7f2
Revises: 8a34c3f94b87
Create Date: 2026-08-28 17:59:32.867064

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "c770d7aac7f2"
down_revision: str = "8a34c3f94b87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "processed_commands",
        sa.Column("actor_identity_user_id", UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        "processed_commands",
        sa.Column("command_name", sa.String(length=64), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("processed_commands", "actor_identity_user_id")
    op.drop_column("processed_commands", "command_name")
