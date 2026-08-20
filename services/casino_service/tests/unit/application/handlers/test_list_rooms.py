import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime

from src.casino_service.application.handlers.list_rooms import ListRoomsHandler
from src.casino_service.application.queries.list_rooms import ListRoomsQuery
from src.casino_service.application.read_models import RoomReadModel


@pytest.mark.asyncio
async def test_list_rooms_success():
    read_repo = AsyncMock()
    room1 = RoomReadModel(
        id=uuid4(),
        name="Room1",
        game_type="poker",
        visibility="public",
        capacity=6,
        owner_player_id=uuid4(),
        participants_count=0,
        status="active",
        is_system=False,
        revision=1,
        invite_token_hash=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        closed_at=None,
    )
    read_repo.list.return_value = ([room1], None)

    handler = ListRoomsHandler(read_repo)
    query = ListRoomsQuery(limit=10)

    items, next_cursor = await handler.handle(query)

    assert len(items) == 1
    assert items[0].id == room1.id
    assert next_cursor is None
    read_repo.list.assert_called_once_with(
        game_type=None,
        visibility=None,
        status=None,
        limit=10,
        cursor=None,
    )


@pytest.mark.asyncio
async def test_list_rooms_limit_clamped():
    read_repo = AsyncMock()
    read_repo.list.return_value = ([], None)

    handler = ListRoomsHandler(read_repo)

    # limit слишком маленький
    query = ListRoomsQuery(limit=0)
    await handler.handle(query)
    assert read_repo.list.call_args[1]["limit"] == 1

    # limit слишком большой
    query = ListRoomsQuery(limit=200)
    await handler.handle(query)
    assert read_repo.list.call_args[1]["limit"] == 100


@pytest.mark.asyncio
async def test_list_rooms_with_filters():
    read_repo = AsyncMock()
    read_repo.list.return_value = ([], None)

    handler = ListRoomsHandler(read_repo)
    query = ListRoomsQuery(
        game_type="poker",
        visibility="public",
        status="active",
        limit=20,
        cursor="some_cursor",
    )

    await handler.handle(query)

    read_repo.list.assert_called_once_with(
        game_type="poker",
        visibility="public",
        status="active",
        limit=20,
        cursor="some_cursor",
    )


@pytest.mark.asyncio
async def test_list_rooms_cursor_pagination():
    read_repo = AsyncMock()
    # Возвращаем два элемента и следующий курсор
    rooms = [
        RoomReadModel(
            id=uuid4(),
            name="Room1",
            game_type="poker",
            visibility="public",
            capacity=6,
            owner_player_id=uuid4(),
            participants_count=1,
            status="active",
            is_system=False,
            revision=1,
            invite_token_hash=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            closed_at=None,
        ),
        RoomReadModel(
            id=uuid4(),
            name="Room2",
            game_type="poker",
            visibility="public",
            capacity=6,
            owner_player_id=uuid4(),
            participants_count=2,
            status="active",
            is_system=False,
            revision=1,
            invite_token_hash=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            closed_at=None,
        ),
    ]
    read_repo.list.return_value = (rooms, "next_cursor_value")

    handler = ListRoomsHandler(read_repo)
    query = ListRoomsQuery(limit=2)

    items, next_cursor = await handler.handle(query)

    assert len(items) == 2
    assert next_cursor == "next_cursor_value"