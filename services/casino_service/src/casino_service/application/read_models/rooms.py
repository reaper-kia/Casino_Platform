from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from casino_service.domain.enums import (
    CasinoPlayerStatus,
    ConnectionStatus,
    GameType,
    MembershipStatus,
    RoomStatus,
    RoomVisibility,
)


@dataclass(frozen=True)
class CasinoPlayerReadModel:
    identity_user_id: UUID

    id: UUID
    nickname: str | None
    avatar_url: str | None
    status: CasinoPlayerStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ParticipantReadModel:
    player: CasinoPlayerReadModel
    room_id: UUID
    player_id: UUID
    seat: int

    id: UUID
    membership_status: MembershipStatus
    connection_status: ConnectionStatus
    joined_at: datetime
    disconnected_at: datetime | None
    reconnect_deadline: datetime | None
    left_at: datetime | None


@dataclass(frozen=True)
class RoomReadModel:
    name: str
    game_type: GameType
    visibility: RoomVisibility
    capacity: int
    owner_player_id: UUID | None
    participants_count: int
    id: UUID
    status: RoomStatus
    is_system: bool
    revision: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None


@dataclass
class RoomSnapshot:
    room: RoomReadModel
    participants: list[ParticipantReadModel]
    server_time: datetime
