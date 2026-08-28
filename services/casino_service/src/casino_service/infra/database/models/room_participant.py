from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from casino_service.domain.enums import ConnectionStatus, MembershipStatus
from casino_service.infra.database.models.casino_player import CasinoPlayerModel
from casino_service.infra.database.models.room import RoomModel
from casino_service.infra.database.session import Base


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

    disconnected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reconnect_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    left_at: Mapped[datetime | None] = mapped_column(
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
