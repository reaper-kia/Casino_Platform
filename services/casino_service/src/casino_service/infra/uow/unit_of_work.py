from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from casino_service.application.ports.casino_player_repository import CasinoPlayerRepository
from casino_service.application.ports.processed_command_repository import ProcessedCommandRepository
from casino_service.application.ports.room_read_repository import RoomReadRepository
from casino_service.application.ports.room_repository import RoomRepository
from casino_service.infra.database.repositories.casino_player import (
    SQLAlchemyCasinoPlayerRepository,
)
from casino_service.infra.database.repositories.processed_command import (
    SQLAlchemyProcessedCommandRepository,
)
from casino_service.infra.database.repositories.room import SQLAlchemyRoomRepository
from casino_service.infra.database.repositories.room_read import SQLAlchemyRoomReadRepository


class SQLAlchemyUnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self.rooms: RoomRepository | None = None
        self.rooms_read: RoomReadRepository | None = None
        self.casino_players: CasinoPlayerRepository | None = None
        self.processed_commands: ProcessedCommandRepository | None = None

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.rooms = SQLAlchemyRoomRepository(self.session)
        self.rooms_read = SQLAlchemyRoomReadRepository(self.session)
        self.casino_players = SQLAlchemyCasinoPlayerRepository(self.session)
        self.processed_commands = SQLAlchemyProcessedCommandRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        if self.session:
            await self.session.close()

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
