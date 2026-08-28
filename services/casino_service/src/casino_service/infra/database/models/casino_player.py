from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from casino_service.domain.enums import CasinoPlayerStatus
from casino_service.infra.database.models.room import RoomModel
from casino_service.infra.database.models.room_participant import RoomParticipantModel
from casino_service.infra.database.session import Base


class CasinoPlayerModel(Base):
    __tablename__ = "casino_players"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    identity_user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
    )
    status: Mapped[CasinoPlayerStatus] = mapped_column(
        SQLEnum(
            CasinoPlayerStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        default=CasinoPlayerStatus.ACTIVE,
    )
    nickname: Mapped[str] = mapped_column(
        String(64),
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

    owned_rooms: Mapped[list["RoomModel"]] = relationship(
        back_populates="owner",
        lazy="selectin",
    )
    participations: Mapped[list["RoomParticipantModel"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
