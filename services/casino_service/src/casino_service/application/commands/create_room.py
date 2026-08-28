from dataclasses import dataclass
from uuid import UUID

from casino_service.domain.enums import GameType, RoomVisibility
from casino_service.domain.exceptions import (
    InvalidGameTypeError,
    InvalidRoomCapacityError,
    InvalidRoomNameError,
    InvalidRoomVisibilityError,
)


@dataclass(frozen=True, slots=True)
class CreateRoomCommand:
    actor_identity_user_id: UUID
    idempotency_key: UUID
    name: str
    game_type: GameType
    visibility: RoomVisibility
    capacity: int

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise InvalidRoomNameError("Room name cannot be empty")
        if self.capacity <= 0:
            raise InvalidRoomCapacityError("Room capacity must be positive")
        if self.game_type not in GameType:
            raise InvalidGameTypeError(f"Unsupported game type: {self.game_type}")
        if self.visibility not in RoomVisibility:
            raise InvalidRoomVisibilityError(f"Unsupported visibility: {self.visibility}")
