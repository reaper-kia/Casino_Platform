import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from casino_service.application.handlers.get_room_snapshot import GetRoomSnapshotHandler
from casino_service.application.queries.get_room_snapshot import GetRoomSnapshotQuery
from casino_service.application.read_models import (
    RoomSnapshot,
    RoomReadModel,
    ParticipantReadModel,
    CasinoPlayerReadModel,
)
from casino_service.domain.enums import (
    GameType,
    RoomVisibility,
    RoomStatus,
    CasinoPlayerStatus,
    MembershipStatus,
    ConnectionStatus,
)
from casino_service.domain.exceptions import RoomNotFoundError


class FakeRoomReadRepository:
    def __init__(self):
        self.snapshots = {}
        self.calls = []

    async def list(self, game_type, visibility, status, limit, cursor):
        return [], None

    async def get_active_participants(self, room_id):
        return []

    async def count_active_participants(self, room_id):
        return 0

    async def get_snapshot(self, room_id):
        self.calls.append(room_id)
        return self.snapshots.get(room_id)


@pytest.mark.asyncio
async def test_get_room_snapshot_success():
    room_id = uuid4()
    player_id = uuid4()
    participant_id = uuid4()

    player_read = CasinoPlayerReadModel(
        identity_user_id=uuid4(),
        id=player_id,
        nickname="Player1",
        avatar_url=None,
        status=CasinoPlayerStatus.ACTIVE,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    participant_read = ParticipantReadModel(
        player=player_read,
        room_id=room_id,
        player_id=player_id,
        seat=1,
        id=participant_id,
        membership_status=MembershipStatus.ACTIVE,
        connection_status=ConnectionStatus.CONNECTED,
        joined_at=datetime.now(UTC),
        disconnected_at=None,
        reconnect_deadline=None,
        left_at=None,
    )

    room_read = RoomReadModel(
        id=room_id,
        name="Test Room",
        game_type=GameType.CRASH,
        visibility=RoomVisibility.PUBLIC,
        capacity=6,
        owner_player_id=player_id,
        status=RoomStatus.OPEN,
        is_system=False,
        revision=1,
        participants_count=1,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        closed_at=None,
    )

    snapshot = RoomSnapshot(
        room=room_read,
        participants=[participant_read],
        server_time=datetime.now(UTC),
        # revision отсутствует, если его нет в read_models
    )

    repo = FakeRoomReadRepository()
    repo.snapshots[room_id] = snapshot

    handler = GetRoomSnapshotHandler(repo)
    query = GetRoomSnapshotQuery(room_id=room_id)

    result = await handler.handle(query)

    assert result.room.id == room_id
    assert len(result.participants) == 1
    assert result.participants[0].player.nickname == "Player1"
    assert result.server_time is not None
    assert result.server_time.tzinfo is not None


@pytest.mark.asyncio
async def test_get_room_snapshot_not_found():
    repo = FakeRoomReadRepository()
    handler = GetRoomSnapshotHandler(repo)
    query = GetRoomSnapshotQuery(room_id=uuid4())

    with pytest.raises(RoomNotFoundError):
        await handler.handle(query)

    assert repo.calls[0] == query.room_id
