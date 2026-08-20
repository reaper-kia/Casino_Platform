from src.casino_service.application.ports.room_repository import (
    RoomRepository,
    RoomReadRepository,
    CasinoPlayerRepository,
    ProcessedCommandRepository,
)

class SQLAlchemyRoomRepository(RoomRepository):
    pass

class SQLAlchemyRoomReadRepository(RoomReadRepository):
    pass

class SQLAlchemyCasinoPlayerRepository(CasinoPlayerRepository):
    pass

class SQLAlchemyProcessedCommandRepository(ProcessedCommandRepository):
    pass

from .repositories import (
    SQLAlchemyRoomRepository,
    SQLAlchemyRoomReadRepository,
    SQLAlchemyCasinoPlayerRepository,
    SQLAlchemyProcessedCommandRepository,
)