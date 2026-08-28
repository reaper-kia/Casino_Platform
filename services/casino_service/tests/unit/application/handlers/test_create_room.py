import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from casino_service.application.commands.create_room import CreateRoomCommand
from casino_service.application.handlers.create_room import CreateRoomHandler
from casino_service.application.results.create_room import CreateRoomResult
from casino_service.domain.entities import Room, CasinoPlayer, ProcessedCommand
from casino_service.domain.enums import GameType, RoomVisibility, CasinoPlayerStatus
from casino_service.domain.exceptions import (
    PlayerNotFoundError,
    IdempotencyConflictError,
    InvalidRoomNameError,
    InvalidRoomCapacityError,
)


# ---------- Fake репозитории ----------
class FakeRoomRepository:
    def __init__(self):
        self._rooms = {}

    async def add(self, room):
        self._rooms[room.id] = room

    async def get_by_id(self, room_id):
        return self._rooms.get(room_id)

    async def save(self, room):
        pass


class FakeCasinoPlayerRepository:
    def __init__(self):
        self._players = {}

    async def find_by_identity_user_id(self, identity_user_id):
        return self._players.get(identity_user_id)


class FakeProcessedCommandRepository:
    def __init__(self):
        self._commands = {}

    async def find_by_key(self, key, actor_identity_user_id, command_name):
        return self._commands.get((key, actor_identity_user_id, command_name))

    async def save(self, cmd):
        self._commands[(cmd.key, cmd.actor_identity_user_id, cmd.command_name)] = cmd


# ---------- Fake Unit of Work ----------
class FakeUnitOfWork:
    def __init__(self):
        self.rooms = FakeRoomRepository()
        self.casino_players = FakeCasinoPlayerRepository()
        self.processed_commands = FakeProcessedCommandRepository()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    def add_casino_player(self, player: CasinoPlayer):
        self.casino_players._players[player.identity_user_id] = player

    def add_room(self, room: Room):
        self.rooms._rooms[room.id] = room

    def add_processed_command(self, cmd: ProcessedCommand):
        self.processed_commands._commands[
            (cmd.key, cmd.actor_identity_user_id, cmd.command_name)
        ] = cmd


@pytest.fixture
def fake_uow():
    return FakeUnitOfWork()


@pytest.fixture
def handler(fake_uow):
    return CreateRoomHandler(fake_uow)


@pytest.mark.asyncio
async def test_create_room_public_success(handler, fake_uow):
    actor_id = uuid4()
    player_id = uuid4()
    player = CasinoPlayer(
        identity_user_id=actor_id,
        id=player_id,
        nickname="test",
        status=CasinoPlayerStatus.ACTIVE,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    fake_uow.add_casino_player(player)

    cmd = CreateRoomCommand(
        actor_identity_user_id=actor_id,
        idempotency_key=uuid4(),
        name="Test Room",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
    )

    result: CreateRoomResult = await handler.handle(cmd)

    assert isinstance(result, CreateRoomResult)
    assert result.room is not None
    assert result.invite_token is None
    assert result.room.name == "Test Room"
    assert result.room.visibility == RoomVisibility.PUBLIC
    assert result.room.capacity == 6
    assert fake_uow.committed is True

    # Проверяем, что ProcessedCommand сохранён
    key = (cmd.idempotency_key, cmd.actor_identity_user_id, "CreateRoom")
    assert key in fake_uow.processed_commands._commands


@pytest.mark.asyncio
async def test_create_room_private_success(handler, fake_uow):
    actor_id = uuid4()
    player_id = uuid4()
    player = CasinoPlayer(
        identity_user_id=actor_id,
        id=player_id,
        nickname="test",
        status=CasinoPlayerStatus.ACTIVE,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    fake_uow.add_casino_player(player)

    cmd = CreateRoomCommand(
        actor_identity_user_id=actor_id,
        idempotency_key=uuid4(),
        name="Private Room",
        game_type=GameType.ROULETTE,
        visibility=RoomVisibility.PRIVATE,
        capacity=4,
    )

    result = await handler.handle(cmd)

    assert result.invite_token is not None
    assert result.room.invite_token_hash is not None
    assert result.room.invite_token_hash != result.invite_token
    assert fake_uow.committed is True


@pytest.mark.asyncio
async def test_create_room_idempotency_same_payload(handler, fake_uow):
    actor_id = uuid4()
    player_id = uuid4()
    player = CasinoPlayer(
        identity_user_id=actor_id,
        id=player_id,
        nickname="test",
        status=CasinoPlayerStatus.ACTIVE,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    fake_uow.add_casino_player(player)

    idempotency_key = uuid4()
    cmd = CreateRoomCommand(
        actor_identity_user_id=actor_id,
        idempotency_key=idempotency_key,
        name="Test Room",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
    )

    result1 = await handler.handle(cmd)
    result2 = await handler.handle(cmd)

    assert result2.room.id == result1.room.id
    assert len(fake_uow.rooms._rooms) == 1
    key = (idempotency_key, actor_id, "CreateRoom")
    assert len(fake_uow.processed_commands._commands) == 1


@pytest.mark.asyncio
async def test_create_room_idempotency_conflict(handler, fake_uow):
    actor_id = uuid4()
    player_id = uuid4()
    player = CasinoPlayer(
        identity_user_id=actor_id,
        id=player_id,
        nickname="test",
        status=CasinoPlayerStatus.ACTIVE,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    fake_uow.add_casino_player(player)

    idempotency_key = uuid4()
    cmd1 = CreateRoomCommand(
        actor_identity_user_id=actor_id,
        idempotency_key=idempotency_key,
        name="Room1",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
    )

    await handler.handle(cmd1)

    cmd2 = CreateRoomCommand(
        actor_identity_user_id=actor_id,
        idempotency_key=idempotency_key,
        name="Room2",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
    )

    with pytest.raises(IdempotencyConflictError):
        await handler.handle(cmd2)

    assert len(fake_uow.rooms._rooms) == 1


@pytest.mark.asyncio
async def test_create_room_player_not_found(handler, fake_uow):
    actor_id = uuid4()
    cmd = CreateRoomCommand(
        actor_identity_user_id=actor_id,
        idempotency_key=uuid4(),
        name="Test",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
    )

    with pytest.raises(PlayerNotFoundError):
        await handler.handle(cmd)

    assert fake_uow.committed is False
    assert len(fake_uow.rooms._rooms) == 0


@pytest.mark.asyncio
async def test_create_room_invalid_name():
    with pytest.raises(InvalidRoomNameError):
        CreateRoomCommand(
            actor_identity_user_id=uuid4(),
            idempotency_key=uuid4(),
            name="   ",
            game_type=GameType.CRASH,
            visibility=RoomVisibility.PUBLIC,
            capacity=6,
        )


@pytest.mark.asyncio
async def test_create_room_invalid_capacity():
    with pytest.raises(InvalidRoomCapacityError):
        CreateRoomCommand(
            actor_identity_user_id=uuid4(),
            idempotency_key=uuid4(),
            name="Test",
            game_type=GameType.CRASH,
            visibility=RoomVisibility.PUBLIC,
            capacity=0,
        )
