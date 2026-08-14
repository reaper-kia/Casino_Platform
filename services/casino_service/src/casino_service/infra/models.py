from datetime import datetime, UTC
from decimal import Decimal
from enum import StrEnum
from typing import Optional
from uuid import UUID, uuid4

from casino_service.domain.enums import ConnectionStatus, GameType, MembershipStatus, RoomStatus, RoomVisibility
from sqlalchemy import CheckConstraint, String, Integer, DateTime, ForeignKey, Index, Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from casino_service.infra.database import Base

class CasinoPlayerModel(Base):
    __tablename__ = "casino_players"

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
        default=uuid4,
    )

    identity_user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
    )
    
    nickname: Mapped[str] = mapped_column(String(64), nullable=False,)
    
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

    owned_rooms: Mapped[list["RoomModel"]] = relationship(
        back_populates="owner",
        lazy="selectin",
    )
    participations: Mapped[list["RoomParticipantModel"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

class RoomModel(Base):
    __tablename__ = "casino_rooms"

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
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

class RoomParticipantModel(Base):
    __tablename__ = "casino_room_participants"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    room_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("casino_rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    player_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("casino_players.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    seat: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    membership_status: Mapped[MembershipStatus] = mapped_column(
        SQLEnum(
            MembershipStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=MembershipStatus.ACTIVE,
        index=True,
    )

    connection_status: Mapped[ConnectionStatus] = mapped_column(
        SQLEnum(
            ConnectionStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=ConnectionStatus.CONNECTED,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    disconnected_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reconnect_deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    left_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    room: Mapped["RoomModel"] = relationship(
        back_populates="participants",
        lazy="selectin",
    )
    player: Mapped["CasinoPlayerModel"] = relationship(
        back_populates="participations",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint(
            "seat >= 1",
            name="check_casino_room_participants_seat_min",
        ),
        # Уникальное свободное место для активных участников
        Index(
            "uq_casino_room_participants_active_room_seat",
            "room_id",
            "seat",
            unique=True,
            postgresql_where=(membership_status == MembershipStatus.ACTIVE),
        ),
        # Уникальный активный игрок в комнате
        Index(
            "uq_casino_room_participants_active_room_player",
            "room_id",
            "player_id",
            unique=True,
            postgresql_where=(membership_status == MembershipStatus.ACTIVE),
        ),
    )