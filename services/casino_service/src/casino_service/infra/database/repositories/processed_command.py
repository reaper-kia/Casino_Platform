from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from casino_service.application.ports.processed_command_repository import ProcessedCommandRepository
from casino_service.domain.entities import ProcessedCommand
from casino_service.infra.database.mappings import (
    processed_command_domain_to_model,
    processed_command_model_to_domain,
)
from casino_service.infra.database.models.processed_command import ProcessedCommandModel


class SQLAlchemyProcessedCommandRepository(ProcessedCommandRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_key(self, key: UUID) -> ProcessedCommand | None:
        stmt = select(ProcessedCommandModel).where(ProcessedCommandModel.key == key)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return processed_command_model_to_domain(model)

    async def save(self, processed_command: ProcessedCommand) -> None:
        model = processed_command_domain_to_model(processed_command)
        self._session.add(model)
