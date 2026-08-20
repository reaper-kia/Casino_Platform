from datetime import datetime, UTC
from ..queries.get_room_snapshot import GetRoomSnapshotQuery
from ..ports.room_repository import RoomReadRepository
from ..read_models import RoomSnapshot
from ...domain.exceptions import RoomNotFoundError


class GetRoomSnapshotHandler:
    def __init__(self, read_repo: RoomReadRepository):
        self._read_repo = read_repo

    async def handle(self, query: GetRoomSnapshotQuery) -> RoomSnapshot:
        snapshot = await self._read_repo.get_snapshot(query.room_id)
        if snapshot is None:
            raise RoomNotFoundError(f"Room {query.room_id} not found")
        return RoomSnapshot(
            room=snapshot.room,
            participants=snapshot.participants,
            server_time=datetime.now(UTC),
        )