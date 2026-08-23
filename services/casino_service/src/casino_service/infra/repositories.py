# src/casino_service/infra/repositories.py

from uuid import UUID
from datetime import datetime, UTC
from typing import List, Optional, Tuple
from decimal import Decimal

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.casino_service.application.ports.room_repository import (
    RoomRepository,
    CasinoPlayerRepository,
    ProcessedCommandRepository,
)
from src.casino_service.application.ports.room_repository import RoomReadRepository
from src.casino_service.application.read_models import (
    RoomReadModel,
    ParticipantReadModel,
    CasinoPlayerReadModel,
    RoomSnapshot,
)
from src.casino_service.domain.entities import Room, CasinoPlayer, ProcessedCommand, RoomParticipant
from src.casino_service.domain.enums import (
    GameType,
    RoomVisibility,
    RoomStatus,
    CasinoPlayerStatus,
    MembershipStatus,
    ConnectionStatus,
)
from src.casino_service.infra.models import (
    RoomModel,
    CasinoPlayerModel,
    RoomParticipantModel,
    ProcessedCommandModel,
)


def room_model_to_domain(model: RoomModel) -> Room:
    return Room(
        id=model.id,
        name=model.name,
        game_type=model.game_type,
        visibility=model.visibility,
        capacity=model.capacity,
        owner_player_id=model.owner_player_id,
        status=model.status,
        is_system=model.is_system,
        revision=model.revision,
        invite_token_hash=model.invite_token_hash,
        created_at=model.created_at,
        updated_at=model.updated_at,
        closed_at=model.closed_at,
    )


def room_domain_to_model(room: Room) -> RoomModel:
    return RoomModel(
        id=room.id,
        name=room.name,
        game_type=room.game_type,
        visibility=room.visibility,
        capacity=room.capacity,
        owner_player_id=room.owner_player_id,
        status=room.status,
        is_system=room.is_system,
        revision=room.revision,
        invite_token_hash=room.invite_token_hash,
        created_at=room.created_at,
        updated_at=room.updated_at,
        closed_at=room.closed_at,
    )


def casino_player_model_to_domain(model: CasinoPlayerModel) -> CasinoPlayer:
    return CasinoPlayer(
        id=model.id,
        identity_user_id=model.identity_user_id,
        nickname=model.nickname,
        avatar_url=model.avatar_url,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def processed_command_model_to_domain(model: ProcessedCommandModel) -> ProcessedCommand:
    return ProcessedCommand(
        key=model.key,
        payload_hash=model.payload_hash,
        result_room_id=model.result_room_id,
        created_at=model.created_at,
    )


def processed_command_domain_to_model(cmd: ProcessedCommand) -> ProcessedCommandModel:
    return ProcessedCommandModel(
        key=cmd.key,
        payload_hash=cmd.payload_hash,
        result_room_id=cmd.result_room_id,
        created_at=cmd.created_at or datetime.now(UTC),
    )


def room_model_to_read_model(model: RoomModel, participants_count: int = 0) -> RoomReadModel:
    return RoomReadModel(
        id=model.id,
        name=model.name,
        game_type=model.game_type,
        visibility=model.visibility,
        capacity=model.capacity,
        owner_player_id=model.owner_player_id,
        status=model.status,
        is_system=model.is_system,
        revision=model.revision,
        invite_token_hash=model.invite_token_hash,
        created_at=model.created_at,
        updated_at=model.updated_at,
        closed_at=model.closed_at,
        participants_count=participants_count,
    )


def participant_model_to_read_model(
    participant_model: RoomParticipantModel,
    player_model: CasinoPlayerModel,
) -> ParticipantReadModel:
    player_read = CasinoPlayerReadModel(
        id=player_model.id,
        identity_user_id=player_model.identity_user_id,
        nickname=player_model.nickname,
        avatar_url=player_model.avatar_url,
        status=player_model.status,
        created_at=player_model.created_at,
        updated_at=player_model.updated_at,
    )
    return ParticipantReadModel(
        id=participant_model.id,
        room_id=participant_model.room_id,
        player_id=participant_model.player_id,
        player=player_read,
        seat=participant_model.seat,
        membership_status=participant_model.membership_status,
        connection_status=participant_model.connection_status,
        joined_at=participant_model.joined_at,
        disconnected_at=participant_model.disconnected_at,
        reconnect_deadline=participant_model.reconnect_deadline,
        left_at=participant_model.left_at,
    )



class SQLAlchemyRoomRepository(RoomRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, room: Room) -> None:
        model = room_domain_to_model(room)
        self._session.add(model)

    async def get_by_id(self, room_id: UUID) -> Optional[Room]:
        stmt = select(RoomModel).where(RoomModel.id == room_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return room_model_to_domain(model)

    async def save(self, room: Room) -> None:
        stmt = select(RoomModel).where(RoomModel.id == room.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError(f"Room with id {room.id} not found")

        model.name = room.name
        model.game_type = room.game_type
        model.visibility = room.visibility
        model.capacity = room.capacity
        model.owner_player_id = room.owner_player_id
        model.status = room.status
        model.is_system = room.is_system
        model.revision = room.revision
        model.invite_token_hash = room.invite_token_hash
        model.updated_at = room.updated_at
        model.closed_at = room.closed_at


class SQLAlchemyCasinoPlayerRepository(CasinoPlayerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_identity_user_id(self, identity_user_id: UUID) -> Optional[CasinoPlayer]:
        stmt = select(CasinoPlayerModel).where(CasinoPlayerModel.identity_user_id == identity_user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return casino_player_model_to_domain(model)


class SQLAlchemyProcessedCommandRepository(ProcessedCommandRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_key(self, key: UUID) -> Optional[ProcessedCommand]:
        stmt = select(ProcessedCommandModel).where(ProcessedCommandModel.key == key)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return processed_command_model_to_domain(model)

    async def save(self, processed_command: ProcessedCommand) -> None:
        model = processed_command_domain_to_model(processed_command)
        self._session.add(model)



# Read


class SQLAlchemyRoomReadRepository(RoomReadRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(
        self,
        game_type: Optional[str],
        visibility: Optional[str],
        status: Optional[str],
        limit: int,
        cursor: Optional[str],
    ) -> Tuple[List[RoomReadModel], Optional[str]]:
        query = select(RoomModel)

        # 2. Фильтры
        if game_type:
            query = query.where(RoomModel.game_type == game_type)
        if visibility:
            query = query.where(RoomModel.visibility == visibility)
        if status:
            query = query.where(RoomModel.status == status)

        if cursor:
            try:
                cursor_uuid = UUID(cursor)
                query = query.where(RoomModel.id < cursor_uuid)
            except ValueError:
                pass

        query = query.order_by(RoomModel.id.desc()).limit(limit + 1)

        result = await self._session.execute(query)
        room_models = result.scalars().all()

        # 5. Вычисляем has_more и обрезаем до limit
        has_more = len(room_models) > limit
        room_models = room_models[:limit]

        # 6. Для каждой комнаты считаем количество активных участников
        room_ids = [r.id for r in room_models]
        participants_counts = {}
        if room_ids:
            count_stmt = (
                select(
                    RoomParticipantModel.room_id,
                    func.count().label("cnt")
                )
                .where(
                    and_(
                        RoomParticipantModel.room_id.in_(room_ids),
                        RoomParticipantModel.membership_status == "active",  # или "ACTIVE" в зависимости от enum
                    )
                )
                .group_by(RoomParticipantModel.room_id)
            )
            count_result = await self._session.execute(count_stmt)
            for row in count_result:
                participants_counts[row.room_id] = row.cnt

        # 7. Собираем read-модели
        items = []
        for model in room_models:
            count = participants_counts.get(model.id, 0)
            items.append(room_model_to_read_model(model, count))

        # 8. next_cursor – последний id (если есть ещё)
        next_cursor = str(room_models[-1].id) if has_more and room_models else None
        return items, next_cursor

    async def get_active_participants(self, room_id: UUID) -> List[ParticipantReadModel]:
        # JOIN RoomParticipant + CasinoPlayer
        stmt = (
            select(RoomParticipantModel, CasinoPlayerModel)
            .join(CasinoPlayerModel, RoomParticipantModel.player_id == CasinoPlayerModel.id)
            .where(
                and_(
                    RoomParticipantModel.room_id == room_id,
                    RoomParticipantModel.membership_status == "active",  # активные участники
                )
            )
        )
        result = await self._session.execute(stmt)
        rows = result.all()
        participants = []
        for participant_model, player_model in rows:
            participants.append(participant_model_to_read_model(participant_model, player_model))
        return participants

    async def count_active_participants(self, room_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(RoomParticipantModel)
            .where(
                and_(
                    RoomParticipantModel.room_id == room_id,
                    RoomParticipantModel.membership_status == "active",
                )
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one() or 0

    async def get_snapshot(self, room_id: UUID) -> Optional[RoomSnapshot]:
        # 1. Получаем комнату
        room_stmt = select(RoomModel).where(RoomModel.id == room_id)
        room_result = await self._session.execute(room_stmt)
        room_model = room_result.scalar_one_or_none()
        if room_model is None:
            return None

        # 2. Получаем активных участников с игроками
        participants = await self.get_active_participants(room_id)

        # 3. Формируем RoomReadModel с participants_count
        room_read = room_model_to_read_model(room_model, len(participants))

        # 4. Собираем снапшот (revision берём из комнаты)
        snapshot = RoomSnapshot(
            room=room_read,
            participants=participants,
            revision=room_model.revision,
            server_time=datetime.now(UTC),  # будет перезаписано в хэндлере
        )
        return snapshot