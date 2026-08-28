from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.entities import Room


class RoomRepository(ABC):
    @abstractmethod
    async def add(self, room: Room) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, room_id: UUID) -> Room | None:
        pass

    @abstractmethod
    async def save(self, room: Room) -> None:
        pass
