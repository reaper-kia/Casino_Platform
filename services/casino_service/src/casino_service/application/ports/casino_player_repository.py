from abc import ABC, abstractmethod
from uuid import UUID

from casino_service.domain.entities import CasinoPlayer


class CasinoPlayerRepository(ABC):
    @abstractmethod
    async def find_by_identity_user_id(self, identity_user_id: UUID) -> CasinoPlayer | None:
        pass
