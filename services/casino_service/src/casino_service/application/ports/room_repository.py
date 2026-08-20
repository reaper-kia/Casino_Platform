from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List, Tuple

from ...domain.entities import Room, CasinoPlayer, ProcessedCommand
from ..read_models import RoomReadModel, ParticipantReadModel, RoomSnapshot


class RoomRepository(ABC):
    """Write-порт для агрегата Room."""
    @abstractmethod
    async def add(self, room: Room) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, room_id: UUID) -> Optional[Room]:
        pass

    @abstractmethod
    async def save(self, room: Room) -> None:
        pass


class RoomReadRepository(ABC):
    @abstractmethod
    async def list(
        self,
        game_type: Optional[str],
        visibility: Optional[str],
        status: Optional[str],
        limit: int,
        cursor: Optional[str],
    ) -> Tuple[List[RoomReadModel], Optional[str]]:
        pass

    @abstractmethod
    async def get_active_participants(self, room_id: UUID) -> List[ParticipantReadModel]:
        pass

    @abstractmethod
    async def count_active_participants(self, room_id: UUID) -> int:
        pass

    @abstractmethod
    async def get_snapshot(self, room_id: UUID) -> Optional[RoomSnapshot]:
        pass


class CasinoPlayerRepository(ABC):
    @abstractmethod
    async def find_by_identity_user_id(self, identity_user_id: UUID) -> Optional[CasinoPlayer]:
        pass


class ProcessedCommandRepository(ABC):
    @abstractmethod
    async def find_by_key(self, key: UUID) -> Optional[ProcessedCommand]:
        pass

    @abstractmethod
    async def save(self, processed_command: ProcessedCommand) -> None:
        pass