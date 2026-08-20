from typing import Tuple, List, Optional
from ..queries.list_rooms import ListRoomsQuery
from ..ports.room_repository import RoomReadRepository
from ..read_models import RoomReadModel


class ListRoomsHandler:
    def __init__(self, read_repo: RoomReadRepository):
        self._read_repo = read_repo

    async def handle(self, query: ListRoomsQuery) -> Tuple[List[RoomReadModel], Optional[str]]:
        limit = max(1, min(100, query.limit))

        items, next_cursor = await self._read_repo.list(
            game_type=query.game_type,
            visibility=query.visibility,
            status=query.status,
            limit=limit,
            cursor=query.cursor,
        )
        return items, next_cursor