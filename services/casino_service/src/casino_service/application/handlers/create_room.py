import hashlib
import json
import secrets
from datetime import UTC, datetime

from casino_service.application.results.create_room import CreateRoomResult
from casino_service.application.ports.unit_of_work import UnitOfWork
from casino_service.domain.entities import ProcessedCommand, Room
from casino_service.domain.exceptions import (
    IdempotencyConflictError,
    InvalidMaxPlayersError,
    InvalidRoomVisibilityError,
    PlayerNotFoundError,
)

from ..commands.create_room import CreateRoomCommand


class CreateRoomHandler:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def handle(self, cmd: CreateRoomCommand) -> CreateRoomResult:
        # Валидация входных данных
        if cmd.visibility not in ("public", "private"):
            raise InvalidRoomVisibilityError("visibility must be 'public' or 'private'")
        if cmd.capacity < 2:  # ← исправлено: max_players → capacity
            raise InvalidMaxPlayersError("capacity must be at least 2")

        async with self._uow as uow:
            existing = await uow.processed_commands.find_by_key(
                key=cmd.idempotency_key,
                actor_identity_user_id=cmd.actor_identity_user_id,
                command_name="CreateRoom",
            )
            payload_hash = self._hash_payload(cmd)

            if existing:
                if existing.payload_hash != payload_hash:
                    raise IdempotencyConflictError(
                        f"Idempotency key {cmd.idempotency_key} used with different payload"
                    )
                room = await uow.rooms.get_by_id(existing.result_room_id)
                if not room:
                    raise RuntimeError(
                        "Inconsistent state: processed command refers to non-existent room"
                    )
                return CreateRoomResult(room=room, invite_token=None)

            player = await uow.casino_players.find_by_identity_user_id(cmd.actor_identity_user_id)
            if not player:
                raise PlayerNotFoundError(
                    f"Player with identity_user_id {cmd.actor_identity_user_id} not found"
                )

            token_hash = None
            raw_token = None
            if cmd.visibility == "private":
                raw_token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

            room = Room.create(
                name=cmd.name,
                owner_id=player.id,
                game_type=cmd.game_type,
                visibility=cmd.visibility,
                token_hash=token_hash,
                capacity=cmd.capacity,
            )

            await uow.rooms.add(room)
            await uow.processed_commands.save(
                ProcessedCommand(
                    key=cmd.idempotency_key,
                    actor_identity_user_id=cmd.actor_identity_user_id,
                    command_name="CreateRoom",
                    payload_hash=payload_hash,
                    result_room_id=room.id,
                    created_at=datetime.now(UTC),
                )
            )
            await uow.commit()
        return CreateRoomResult(room=room, invite_token=raw_token)

    @staticmethod
    def _hash_payload(cmd: CreateRoomCommand) -> str:
        data = {
            "name": cmd.name,
            "game_type": cmd.game_type.value,
            "visibility": cmd.visibility.value,
            "capacity": cmd.capacity,
        }
        return hashlib.sha256(
            json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
