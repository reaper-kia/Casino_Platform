from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from casino_service.application.ports.casino_player_repository import CasinoPlayerRepository
from casino_service.domain.entities import CasinoPlayer
from casino_service.infra.database.mappings import casino_player_model_to_domain
from casino_service.infra.database.models.casino_player import CasinoPlayerModel


class SQLAlchemyCasinoPlayerRepository(CasinoPlayerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_identity_user_id(self, identity_user_id: UUID) -> CasinoPlayer | None:
        stmt = select(CasinoPlayerModel).where(
            CasinoPlayerModel.identity_user_id == identity_user_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return casino_player_model_to_domain(model)
