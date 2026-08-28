from casino_service.application.ports.room_read_repository import RoomReadRepository
from casino_service.application.queries.list_rooms import ListRoomsQuery
from casino_service.application.read_models import RoomReadModel


class ListRoomsHandler:
    def __init__(self, read_repo: RoomReadRepository):
        self._read_repo = read_repo

    async def handle(self, query: ListRoomsQuery) -> tuple[list[RoomReadModel], str | None]:
        # Ограничение limit 1..100
        limit = max(1, min(100, query.limit))

        items, next_cursor = await self._read_repo.list(
            game_type=query.game_type,
            visibility=query.visibility,
            status=query.status,
            limit=limit,
            cursor=query.cursor,
        )
        return items, next_cursor
