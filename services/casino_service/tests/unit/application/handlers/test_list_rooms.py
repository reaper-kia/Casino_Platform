import pytest
from uuid import uuid4
from datetime import datetime, UTC

from casino_service.application.handlers.list_rooms import ListRoomsHandler
from casino_service.application.queries.list_rooms import ListRoomsQuery
from casino_service.application.read_models import RoomReadModel
from casino_service.domain.enums import GameType, RoomVisibility, RoomStatus


class FakeRoomReadRepository:
    def __init__(self, rooms=None):
        self.rooms = rooms or []
        self.calls = []

    async def list(self, game_type, visibility, status, limit, cursor):
        self.calls.append((game_type, visibility, status, limit, cursor))
        filtered = self.rooms
        if game_type is not None:
            filtered = [r for r in filtered if r.game_type == game_type]
        if visibility is not None:
            filtered = [r for r in filtered if r.visibility == visibility]
        if status is not None:
            filtered = [r for r in filtered if r.status == status]
        return filtered[:limit], None

    async def get_active_participants(self, room_id):
        return []

    async def count_active_participants(self, room_id):
        return 0

    async def get_snapshot(self, room_id):
        return None


@pytest.mark.asyncio
async def test_list_rooms_success():
    room = RoomReadModel(
        id=uuid4(),
        name="Room1",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
        owner_player_id=uuid4(),
        status=RoomStatus.OPEN,
        is_system=False,
        revision=1,
        participants_count=0,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        closed_at=None,
    )
    repo = FakeRoomReadRepository(rooms=[room])
    handler = ListRoomsHandler(repo)

    query = ListRoomsQuery(limit=10)
    items, next_cursor = await handler.handle(query)

    assert len(items) == 1
    assert items[0].id == room.id
    assert next_cursor is None
    assert repo.calls[0][3] == 10


@pytest.mark.asyncio
async def test_list_rooms_limit_clamped():
    repo = FakeRoomReadRepository()
    handler = ListRoomsHandler(repo)

    query = ListRoomsQuery(limit=0)
    await handler.handle(query)
    assert repo.calls[0][3] == 1

    query = ListRoomsQuery(limit=200)
    await handler.handle(query)
    assert repo.calls[1][3] == 100


@pytest.mark.asyncio
async def test_list_rooms_with_filters():
    repo = FakeRoomReadRepository()
    handler = ListRoomsHandler(repo)

    query = ListRoomsQuery(
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        status=RoomStatus.OPEN,
        limit=20,
        cursor="some_cursor",
    )
    await handler.handle(query)

    assert repo.calls[0][0] == GameType.CRASH
    assert repo.calls[0][1] == RoomVisibility.PUBLIC
    assert repo.calls[0][2] == RoomStatus.OPEN
    assert repo.calls[0][3] == 20
    assert repo.calls[0][4] == "some_cursor"
