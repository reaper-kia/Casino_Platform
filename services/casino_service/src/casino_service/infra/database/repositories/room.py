from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from casino_service.application.ports.room_repository import RoomRepository
from casino_service.domain.entities import Room
from casino_service.infra.database.models.room import RoomModel
from casino_service.infra.mappings import room_domain_to_model, room_model_to_domain


class SQLAlchemyRoomRepository(RoomRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, room: Room) -> None:
        model = room_domain_to_model(room)
        self._session.add(model)

    async def get_by_id(self, room_id: UUID) -> Room | None:
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
