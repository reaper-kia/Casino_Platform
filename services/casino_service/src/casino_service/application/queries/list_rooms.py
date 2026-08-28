from dataclasses import dataclass

from casino_service.domain.enums import GameType, RoomStatus, RoomVisibility


@dataclass(frozen=True)
class ListRoomsQuery:
    game_type: GameType | None = None
    visibility: RoomVisibility | None = None
    status: RoomStatus | None = None
    limit: int = 20
    cursor: str | None = None
