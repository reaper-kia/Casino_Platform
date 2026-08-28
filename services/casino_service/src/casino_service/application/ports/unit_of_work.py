from abc import ABC, abstractmethod
from typing import Protocol

from casino_service.application.ports.casino_player_repository import CasinoPlayerRepository
from casino_service.application.ports.processed_command_repository import ProcessedCommandRepository
from casino_service.application.ports.room_repository import RoomRepository


class UnitOfWork(ABC):
    rooms: RoomRepository
    casino_players: CasinoPlayerRepository
    processed_commands: ProcessedCommandRepository

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass


class UnitOfWorkFactory(Protocol):
    def __call__(self) -> UnitOfWork: ...
