from dataclasses import dataclass

from casino_service.domain.entities import Room


@dataclass(frozen=True, slots=True)
class CreateRoomResult:
    room: Room
    invite_token: str | None
