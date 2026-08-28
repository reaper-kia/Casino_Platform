from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from casino_service.domain.enums import GameType, RoomStatus, RoomVisibility
from casino_service.infra.database.session import Base
from casino_service.infra.models import CasinoPlayerModel, RoomParticipantModel


class RoomModel(Base):
    __tablename__ = "casino_rooms"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    game_type: Mapped[GameType] = mapped_column(
        SQLEnum(GameType, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        index=True,
    )

    visibility: Mapped[RoomVisibility] = mapped_column(
        SQLEnum(RoomVisibility, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RoomVisibility.PUBLIC,
        index=True,
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
    )

    owner_player_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("casino_players.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[RoomStatus] = mapped_column(
        SQLEnum(RoomStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RoomStatus.OPEN,
        index=True,
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    revision: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    invite_token_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    owner: Mapped["CasinoPlayerModel | None"] = relationship(
        back_populates="owned_rooms",
        lazy="selectin",
    )

    participants: Mapped[list["RoomParticipantModel"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint(
            "capacity > 0",
            name="check_casino_rooms_capacity_positive",
        ),
        CheckConstraint(
            "revision >= 1",
            name="check_casino_rooms_revision_min",
        ),
        CheckConstraint(
            """
            (is_system = TRUE AND owner_player_id IS NULL)
            OR
            (is_system = FALSE AND owner_player_id IS NOT NULL)
            """,
            name="check_casino_rooms_system_owner_policy",
        ),
        Index(
            "ix_casino_rooms_status_visibility_game_type",
            "status",
            "visibility",
            "game_type",
        ),
    )
