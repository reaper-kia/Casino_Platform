import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, UTC  # добавили импорт UTC

from src.casino_service.application.handlers.get_room_snapshot import GetRoomSnapshotHandler
from src.casino_service.application.queries.get_room_snapshot import GetRoomSnapshotQuery
from src.casino_service.application.read_models import RoomSnapshot, RoomReadModel, ParticipantReadModel, CasinoPlayerReadModel
from src.casino_service.domain.exceptions import RoomNotFoundError


@pytest.mark.asyncio
async def test_get_room_snapshot_success():
    read_repo = AsyncMock()
    room_id = uuid4()
    player_id = uuid4()
    participant_id = uuid4()

    snapshot = RoomSnapshot(
        room=RoomReadModel(
            id=room_id,
            name="Test Room",
            game_type="poker",
            visibility="public",
            capacity=6,
            owner_player_id=player_id,
            participants_count=1,
            status="active",
            is_system=False,
            revision=1,  # <--- ДОБАВЛЕНО
            invite_token_hash=None,
            created_at=datetime.now(UTC),  # заменено utcnow() на now(UTC)
            updated_at=datetime.now(UTC),
            closed_at=None,
        ),
        participants=[
            ParticipantReadModel(
                id=participant_id,
                room_id=room_id,
                player_id=player_id,
                player=CasinoPlayerReadModel(
                    identity_user_id=uuid4(),
                    id=player_id,
                    nickname="Player1",
                    avatar_url=None,
                    status="active",
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                ),
                seat=1,
                membership_status="active",
                connection_status="connected",
                joined_at=datetime.now(UTC),
                disconnected_at=None,
                reconnect_deadline=None,
                left_at=None,
            )
        ],
        server_time=datetime.now(UTC),
    )
    read_repo.get_snapshot.return_value = snapshot

    handler = GetRoomSnapshotHandler(read_repo)
    query = GetRoomSnapshotQuery(room_id=room_id)

    result = await handler.handle(query)

    assert result.room.id == room_id
    assert len(result.participants) == 1
    assert result.participants[0].player.nickname == "Player1"
    assert result.server_time is not None
    read_repo.get_snapshot.assert_called_once_with(room_id)


@pytest.mark.asyncio
async def test_get_room_snapshot_not_found():
    read_repo = AsyncMock()
    read_repo.get_snapshot.return_value = None

    handler = GetRoomSnapshotHandler(read_repo)
    query = GetRoomSnapshotQuery(room_id=uuid4())

    with pytest.raises(RoomNotFoundError):
        await handler.handle(query)

    read_repo.get_snapshot.assert_called_once_with(query.room_id)