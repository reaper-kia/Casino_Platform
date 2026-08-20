import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from src.casino_service.domain.enums import GameType, RoomVisibility
from src.casino_service.application.handlers.create_room import CreateRoomHandler
from src.casino_service.application.commands.create_room import CreateRoomCommand
from src.casino_service.domain.entities import Room, CasinoPlayer, ProcessedCommand
from src.casino_service.domain.exceptions import (
    PlayerNotFoundError,
    IdempotencyConflictError,
    InvalidRoomVisibilityError,
    InvalidMaxPlayersError,
)


@pytest.mark.asyncio
async def test_create_room_success():
    # Подготовка
    player_id = uuid4()
    identity_user_id = uuid4()
    idempotency_key = uuid4()
    room_id = uuid4()

    # Моки репозиториев
    room_repo = AsyncMock()
    player_repo = AsyncMock()
    processed_repo = AsyncMock()
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.rooms = room_repo
    uow.casino_players = player_repo
    uow.processed_commands = processed_repo

    # Настройка поведения
    player = CasinoPlayer(id=player_id, identity_user_id=identity_user_id)
    player_repo.find_by_identity_user_id.return_value = player
    processed_repo.find_by_key.return_value = None

    # Хэндлер
    handler = CreateRoomHandler(room_repo, player_repo, processed_repo, uow)

    cmd = CreateRoomCommand(
        idempotency_key=idempotency_key,
        actor_identity_user_id=identity_user_id,
        game_type="poker",
        visibility="public",
        max_players=6,
    )

    # Действие
    room = await handler.handle(cmd)

    # Проверки
    assert room is not None
    assert room.owner_player_id == player_id
    assert room.visibility == "public"
    player_repo.find_by_identity_user_id.assert_called_once_with(identity_user_id)
    room_repo.add.assert_called_once()
    processed_repo.save.assert_called_once()
    uow.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_room_player_not_found():
    room_repo = AsyncMock()
    player_repo = AsyncMock()
    processed_repo = AsyncMock()
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.rooms = room_repo
    uow.casino_players = player_repo
    uow.processed_commands = processed_repo

    player_repo.find_by_identity_user_id.return_value = None

    handler = CreateRoomHandler(room_repo, player_repo, processed_repo, uow)
    handler._hash_payload = lambda _: "some_hash"

    cmd = CreateRoomCommand(
        idempotency_key=uuid4(),
        actor_identity_user_id=uuid4(),
        game_type="poker",
        visibility="public",
        max_players=6,
    )

    processed_repo.find_by_key.return_value = None
    with pytest.raises(PlayerNotFoundError):
        await handler.handle(cmd)

    room_repo.add.assert_not_called()
    processed_repo.save.assert_not_called()
    uow.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_room_idempotency_same_payload():
    player_id = uuid4()
    identity_user_id = uuid4()
    idempotency_key = uuid4()
    room_id = uuid4()

    room_repo = AsyncMock()
    player_repo = AsyncMock()
    processed_repo = AsyncMock()
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.rooms = room_repo
    uow.casino_players = player_repo
    uow.processed_commands = processed_repo

    player = CasinoPlayer(id=player_id, identity_user_id=identity_user_id)
    player_repo.find_by_identity_user_id.return_value = player

    # Создаём существующую запись ProcessedCommand
    existing_cmd = ProcessedCommand(
        key=idempotency_key,
        payload_hash="some_hash",  # будет совпадать с хэшем команды
        result_room_id=room_id,
    )
    processed_repo.find_by_key.return_value = existing_cmd

    # Мокаем, что комната существует
    room = Room(
        id=room_id,
        name="Test Room",
        capacity=6,
        owner_player_id=player_id,
        visibility=RoomVisibility.PUBLIC,
        game_type=GameType.POKER,
    )
    room_repo.get_by_id.return_value = room

    handler = CreateRoomHandler(room_repo, player_repo, processed_repo, uow)
    handler._hash_payload = lambda _: "some_hash"   # <-- добавь эту строку

    # Используем ту же команду, что и при создании
    cmd = CreateRoomCommand(
        idempotency_key=idempotency_key,
        actor_identity_user_id=identity_user_id,
        game_type="poker",
        visibility="public",
        max_players=6,
    )

    result = await handler.handle(cmd)

    assert result.id == room_id
    # Должен вернуть существующую комнату, не создавая новую
    room_repo.add.assert_not_called()
    processed_repo.save.assert_not_called()
    uow.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_room_idempotency_conflict():
    player_id = uuid4()
    identity_user_id = uuid4()
    idempotency_key = uuid4()

    room_repo = AsyncMock()
    player_repo = AsyncMock()
    processed_repo = AsyncMock()
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.rooms = room_repo
    uow.casino_players = player_repo
    uow.processed_commands = processed_repo

    player = CasinoPlayer(id=player_id, identity_user_id=identity_user_id)
    player_repo.find_by_identity_user_id.return_value = player

    existing_cmd = ProcessedCommand(
        key=idempotency_key,
        payload_hash="different_hash",
        result_room_id=uuid4(),
    )
    processed_repo.find_by_key.return_value = existing_cmd

    handler = CreateRoomHandler(room_repo, player_repo, processed_repo, uow)

    cmd = CreateRoomCommand(
        idempotency_key=idempotency_key,
        actor_identity_user_id=identity_user_id,
        game_type="poker",
        visibility="public",
        max_players=6,
    )

    with pytest.raises(IdempotencyConflictError):
        await handler.handle(cmd)

    room_repo.add.assert_not_called()
    processed_repo.save.assert_not_called()
    uow.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_room_invalid_visibility():
    room_repo = AsyncMock()
    player_repo = AsyncMock()
    processed_repo = AsyncMock()
    uow = AsyncMock()
    handler = CreateRoomHandler(room_repo, player_repo, processed_repo, uow)

    cmd = CreateRoomCommand(
        idempotency_key=uuid4(),
        actor_identity_user_id=uuid4(),
        game_type="poker",
        visibility="invalid",
        max_players=6,
    )

    processed_repo.find_by_key.return_value = None
    with pytest.raises(InvalidRoomVisibilityError):
        await handler.handle(cmd)

    player_repo.find_by_identity_user_id.assert_not_called()
    room_repo.add.assert_not_called()
    processed_repo.save.assert_not_called()
    uow.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_room_invalid_max_players():
    room_repo = AsyncMock()
    player_repo = AsyncMock()
    processed_repo = AsyncMock()
    uow = AsyncMock()
    handler = CreateRoomHandler(room_repo, player_repo, processed_repo, uow)

    cmd = CreateRoomCommand(
        idempotency_key=uuid4(),
        actor_identity_user_id=uuid4(),
        game_type="poker",
        visibility="public",
        max_players=1,
    )

    processed_repo.find_by_key.return_value = None
    with pytest.raises(InvalidMaxPlayersError):
        await handler.handle(cmd)

    player_repo.find_by_identity_user_id.assert_not_called()
    room_repo.add.assert_not_called()
    processed_repo.save.assert_not_called()
    uow.commit.assert_not_called()