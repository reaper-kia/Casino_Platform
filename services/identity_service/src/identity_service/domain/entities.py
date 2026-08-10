from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(UTC)


class UserRole(StrEnum):
    PLAYER = "player"
    ADMIN = "admin"


class UserStatus(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    DELETED = "deleted"


@dataclass(slots=True, kw_only=True)
class User:
    email: str
    nickname: str
    password_hash: str

    id: UUID = field(default_factory=uuid4)
    role: UserRole = UserRole.PLAYER
    status: UserStatus = UserStatus.ACTIVE
    password_algorithm: str = "argon2id"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    password_changed_at: datetime = field(default_factory=utc_now)

    def change_password(self, password_hash: str, algorithm: str) -> None:
        self.password_hash = password_hash
        self.password_algorithm = algorithm
        self.password_changed_at = utc_now()
        self.updated_at = self.password_changed_at

    def block(self) -> None:
        self.status = UserStatus.BLOCKED
        self.updated_at = utc_now()


@dataclass(slots=True, kw_only=True)
class RefreshSession:
    user_id: UUID
    token_hash: str
    expires_at: datetime

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    revoked_at: datetime | None = None
    ip_address: str | None = None
    user_agent: str | None = None

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None and self.expires_at > utc_now()

    def revoke(self) -> None:
        if self.revoked_at is None:
            self.revoked_at = utc_now()
