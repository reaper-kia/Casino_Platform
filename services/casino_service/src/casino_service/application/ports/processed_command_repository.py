from abc import ABC, abstractmethod
from uuid import UUID

from casino_service.domain.entities import ProcessedCommand


class ProcessedCommandRepository(ABC):
    @abstractmethod
    async def find_by_key(self, key: UUID) -> ProcessedCommand | None:
        pass

    @abstractmethod
    async def save(self, processed_command: ProcessedCommand) -> None:
        pass
