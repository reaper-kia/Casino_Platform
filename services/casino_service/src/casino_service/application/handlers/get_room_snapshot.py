from datetime import UTC, datetime

from casino_service.application.ports.room_read_repository import RoomReadRepository
from casino_service.application.queries.get_room_snapshot import GetRoomSnapshotQuery
from casino_service.application.read_models import RoomSnapshot
from casino_service.domain.exceptions import RoomNotFoundError


class GetRoomSnapshotHandler:
    def __init__(self, read_repo: RoomReadRepository):
        self._read_repo = read_repo

    async def handle(self, query: GetRoomSnapshotQuery) -> RoomSnapshot:
        snapshot = await self._read_repo.get_snapshot(query.room_id)
        if snapshot is None:
            raise RoomNotFoundError(f"Room {query.room_id} not found")
        snapshot.server_time = datetime.now(UTC)
        return snapshot
