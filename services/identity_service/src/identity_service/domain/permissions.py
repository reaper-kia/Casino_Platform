from enum import StrEnum
from types import MappingProxyType

from identity_service.domain.entities import UserRole


class Permission(StrEnum):
    USERS_READ = "users:read"
    USERS_BLOCK = "users:block"
    LEDGER_READ = "ledger:read"
    BALANCE_ADJUST = "balance:adjust"
    PROMO_MANAGE = "promo:manage"
    CASINO_ROOMS_MANAGE = "casino:rooms:manage"


ROLE_PERMISSIONS = MappingProxyType(
    {
        UserRole.PLAYER: frozenset(),
        UserRole.ADMIN: frozenset(Permission),
    }
)
