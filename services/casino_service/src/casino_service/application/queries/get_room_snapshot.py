from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class GetRoomSnapshotQuery:
    room_id: UUID