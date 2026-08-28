from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from casino_service.application.ports.unit_of_work import UnitOfWorkFactory
from casino_service.infra.uow.unit_of_work import SQLAlchemyUnitOfWork


class SQLAlchemyUnitOfWorkFactory(UnitOfWorkFactory):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    def __call__(self) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(self._session_factory)
