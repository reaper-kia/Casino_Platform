import hashlib
import secrets
from datetime import datetime
from uuid import UUID

from src.casino_service.domain.exceptions import (
    InvalidMaxPlayersError,
    InvalidRoomVisibilityError,
    PlayerNotFoundError,
    IdempotencyConflictError,
)
from src.casino_service.infra.unit_of_work import SQLAlchemyUnitOfWork

from ..commands.create_room import CreateRoomCommand
from ..ports.room_repository import RoomRepository, CasinoPlayerRepository, ProcessedCommandRepository
from ...domain.entities import Room, ProcessedCommand


class CreateRoomHandler:
    def __init__(
        self,
        room_repo: RoomRepository,
        player_repo: CasinoPlayerRepository,
        processed_repo: ProcessedCommandRepository,
        uow: SQLAlchemyUnitOfWork,
    ):
        self._room_repo = room_repo
        self._player_repo = player_repo
        self._processed_repo = processed_repo
        self._uow = uow

    async def handle(self, cmd: CreateRoomCommand) -> Room:
        # 1. Валидация входных данных
        if cmd.visibility not in ("public", "private"):
            raise InvalidRoomVisibilityError("visibility must be 'public' or 'private'")
        if cmd.max_players < 2:
            raise InvalidMaxPlayersError("max_players must be at least 2")

        # 2. Идемпотентность
        existing = await self._processed_repo.find_by_key(cmd.idempotency_key)
        payload_hash = self._hash_payload(cmd)
        if existing:
            if existing.payload_hash != payload_hash:
                raise IdempotencyConflictError(
                    f"Idempotency key {cmd.idempotency_key} used with different payload"
                )
            room = await self._room_repo.get_by_id(existing.result_room_id)
            if not room:
                raise RuntimeError("Inconsistent state: processed command refers to non-existent room")
            return room

        # 3. Поиск игрока
        player = await self._player_repo.find_by_identity_user_id(cmd.actor_identity_user_id)
        if not player:
            raise PlayerNotFoundError(f"Player with identity_user_id {cmd.actor_identity_user_id} not found")

        # 4. Генерация токена для private-комнаты
        token_hash = None
        raw_token = None
        if cmd.visibility == "private":
            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            # raw_token можно вернуть клиенту, но в БД храним только хэш

        # 5. Создание комнаты через фабрику
        room = Room.create(
            owner_id=player.id,
            game_type=cmd.game_type,
            visibility=cmd.visibility,
            token_hash=token_hash,
            max_players=cmd.max_players,
        )

        # 6. Сохранение в одной транзакции
        await self._room_repo.add(room)
        await self._processed_repo.save(
            ProcessedCommand(
                key=cmd.idempotency_key,
                payload_hash=payload_hash,
                result_room_id=room.id,
                created_at=datetime.utcnow(),
            )
        )
        await self._uow.commit()

        # (Опционально: если нужно вернуть сырой токен, можно его вернуть отдельно)
        return room

    @staticmethod
    def _hash_payload(cmd: CreateRoomCommand) -> str:
        payload = f"{cmd.actor_identity_user_id}:{cmd.game_type}:{cmd.visibility}:{cmd.max_players}"
        return hashlib.sha256(payload.encode()).hexdigest()