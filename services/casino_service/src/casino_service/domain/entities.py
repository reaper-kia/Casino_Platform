from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from casino_service.domain.enums import (
    BetStatus,
    CasinoPlayerStatus,
    ConnectionStatus,
    GameType,
    MembershipStatus,
    RoomStatus,
    RoomVisibility,
    RoundActionType,
    RoundStatus,
)
from casino_service.domain.value_objects import Money


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True, kw_only=True)
class CasinoPlayer:
    identity_user_id: UUID

    id: UUID = field(default_factory=uuid4)
    nickname: str | None = None
    avatar_url: str | None = None
    status: CasinoPlayerStatus = CasinoPlayerStatus.ACTIVE
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True, kw_only=True)
class Room:
    name: str
    game_type: GameType
    visibility: RoomVisibility
    capacity: int
    owner_player_id: UUID | None

    id: UUID = field(default_factory=uuid4)
    status: RoomStatus = RoomStatus.OPEN
    is_system: bool = False
    revision: int = 1
    invite_token_hash: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    closed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Room name cannot be empty")

        if self.capacity <= 0:
            raise ValueError("Room capacity must be positive")

        if self.is_system and self.owner_player_id is not None:
            raise ValueError("System room cannot have a player owner")

        if not self.is_system and self.owner_player_id is None:
            raise ValueError("Player-created room must have an owner")

        if (
            self.visibility is RoomVisibility.PRIVATE
            and self.invite_token_hash is None
        ):
            raise ValueError("Private room must have an invite token hash")

    def close(self) -> None:
        if self.status is RoomStatus.CLOSED:
            return

        if self.status is RoomStatus.ARCHIVED:
            raise ValueError("Archived room cannot be closed")

        self.status = RoomStatus.CLOSED
        self.revision += 1
        self.closed_at = utc_now()
        self.updated_at = self.closed_at

    def is_full(self, active_participants: int) -> bool:
        return active_participants >= self.capacity


@dataclass(slots=True, kw_only=True)
class RoomParticipant:
    room_id: UUID
    player_id: UUID
    seat: int

    id: UUID = field(default_factory=uuid4)
    membership_status: MembershipStatus = MembershipStatus.ACTIVE
    connection_status: ConnectionStatus = ConnectionStatus.CONNECTED
    joined_at: datetime = field(default_factory=utc_now)
    disconnected_at: datetime | None = None
    reconnect_deadline: datetime | None = None
    left_at: datetime | None = None

    def mark_disconnected(self, reconnect_deadline: datetime) -> None:
        if self.membership_status is not MembershipStatus.ACTIVE:
            raise ValueError("Inactive participant cannot be disconnected")

        self.connection_status = ConnectionStatus.DISCONNECTED
        self.disconnected_at = utc_now()
        self.reconnect_deadline = reconnect_deadline

    def reconnect(self, now: datetime | None = None) -> None:
        current_time = now or utc_now()

        if self.membership_status is not MembershipStatus.ACTIVE:
            raise ValueError("Participant has already left")

        if (
            self.reconnect_deadline is not None
            and current_time > self.reconnect_deadline
        ):
            raise ValueError("Reconnect grace period expired")

        self.connection_status = ConnectionStatus.CONNECTED
        self.disconnected_at = None
        self.reconnect_deadline = None

    def leave(self) -> None:
        if self.membership_status is MembershipStatus.LEFT:
            return

        self.membership_status = MembershipStatus.LEFT
        self.connection_status = ConnectionStatus.DISCONNECTED
        self.reconnect_deadline = None
        self.left_at = utc_now()


@dataclass(slots=True, kw_only=True)
class FairnessData:
    server_seed_hash: str
    client_seed: str
    nonce: int
    algorithm_version: str

    server_seed: str | None = None


@dataclass(slots=True, kw_only=True)
class Round:
    room_id: UUID
    game_type: GameType
    round_number: int
    configuration_version: str

    id: UUID = field(default_factory=uuid4)
    status: RoundStatus = RoundStatus.SCHEDULED
    revision: int = 1
    fairness: FairnessData | None = None
    result: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    betting_started_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass(slots=True, kw_only=True)
class Bet:
    round_id: UUID
    player_id: UUID
    amount: Money
    selection: dict[str, object]
    idempotency_key: str

    id: UUID = field(default_factory=uuid4)
    wallet_reservation_id: UUID | None = None
    status: BetStatus = BetStatus.PENDING_RESERVATION
    payout_minor: int = 0
    created_at: datetime = field(default_factory=utc_now)
    accepted_at: datetime | None = None
    settled_at: datetime | None = None


@dataclass(slots=True, kw_only=True)
class RoundAction:
    round_id: UUID
    player_id: UUID
    action_type: RoundActionType
    payload: dict[str, object]

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True, kw_only=True)
class ProcessedCommand:
    request_id: str
    request_hash: str
    command_name: str

    id: UUID = field(default_factory=uuid4)
    event_id: UUID | None = None
    response_payload: dict[str, object] = field(default_factory=dict)
    error_code: str | None = None
    completed_at: datetime = field(default_factory=utc_now)