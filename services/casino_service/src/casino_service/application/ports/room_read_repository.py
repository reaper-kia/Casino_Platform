import builtins
from abc import ABC, abstractmethod
from uuid import UUID

from casino_service.application.read_models import ParticipantReadModel, RoomReadModel, RoomSnapshot


class RoomReadRepository(ABC):
    @abstractmethod
    async def list(
        self,
        game_type: str | None,
        visibility: str | None,
        status: str | None,
        limit: int,
        cursor: str | None,
    ) -> tuple[list[RoomReadModel], str | None]:
        pass

    @abstractmethod
    async def get_active_participants(self, room_id: UUID) -> builtins.list[ParticipantReadModel]:
        pass

    @abstractmethod
    async def count_active_participants(self, room_id: UUID) -> int:
        pass

    @abstractmethod
    async def get_snapshot(self, room_id: UUID) -> RoomSnapshot | None:
        pass
