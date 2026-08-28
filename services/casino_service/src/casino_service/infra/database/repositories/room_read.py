import builtins
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from casino_service.application.ports.room_read_repository import RoomReadRepository
from casino_service.application.read_models.rooms import (
    ParticipantReadModel,
    RoomReadModel,
    RoomSnapshot,
)
from casino_service.infra.database.models.casino_player import CasinoPlayerModel
from casino_service.infra.database.models.room import RoomModel
from casino_service.infra.database.models.room_participant import RoomParticipantModel
from casino_service.infra.mappings import participant_model_to_read_model, room_model_to_read_model


class SQLAlchemyRoomReadRepository(RoomReadRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(
        self,
        game_type: str | None,
        visibility: str | None,
        status: str | None,
        limit: int,
        cursor: str | None,
    ) -> tuple[list[RoomReadModel], str | None]:
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
                select(RoomParticipantModel.room_id, func.count().label("cnt"))
                .where(
                    and_(
                        RoomParticipantModel.room_id.in_(room_ids),
                        RoomParticipantModel.membership_status
                        == "active",  # или "ACTIVE" в зависимости от enum
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

    async def get_active_participants(self, room_id: UUID) -> builtins.list[ParticipantReadModel]:
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

    async def get_snapshot(self, room_id: UUID) -> RoomSnapshot | None:
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
