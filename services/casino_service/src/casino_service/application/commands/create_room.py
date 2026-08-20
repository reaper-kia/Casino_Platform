from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateRoomCommand:
    idempotency_key: UUID
    actor_identity_user_id: UUID
    game_type: str
    visibility: str
    max_players: int