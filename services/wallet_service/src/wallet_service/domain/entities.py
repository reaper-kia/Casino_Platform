from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from wallet_service.domain.value_objects import Money


def utc_now() -> datetime:
    return datetime.now(UTC)


class WalletStatus(StrEnum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"


class ReservationStatus(StrEnum):
    ACTIVE = "active"
    SETTLED = "settled"
    RELEASED = "released"
    EXPIRED = "expired"


class LedgerDirection(StrEnum):
    CREDIT = "credit"
    DEBIT = "debit"


class LedgerEntryType(StrEnum):
    INITIAL_GRANT = "initial_grant"
    BET_SETTLEMENT = "bet_settlement"
    BONUS = "bonus"
    ADMIN_ADJUSTMENT = "admin_adjustment"


@dataclass(slots=True, kw_only=True)
class WalletAccount:
    user_id: UUID

    id: UUID = field(default_factory=uuid4)
    currency: str = "USD"
    accounting_balance_minor: int = 0
    status: WalletStatus = WalletStatus.ACTIVE
    version: int = 1
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def credit(self, amount: Money) -> None:
        self._ensure_currency(amount)
        self._ensure_active()

        self.accounting_balance_minor += amount.amount_minor
        self.version += 1
        self.updated_at = utc_now()

    def debit(self, amount: Money) -> None:
        self._ensure_currency(amount)
        self._ensure_active()

        if amount.amount_minor > self.accounting_balance_minor:
            raise ValueError("Insufficient accounting balance")

        self.accounting_balance_minor -= amount.amount_minor
        self.version += 1
        self.updated_at = utc_now()

    def _ensure_currency(self, amount: Money) -> None:
        if amount.currency != self.currency:
            raise ValueError("Currency mismatch")

    def _ensure_active(self) -> None:
        if self.status is not WalletStatus.ACTIVE:
            raise ValueError("Wallet is not active")


@dataclass(slots=True, kw_only=True)
class Reservation:
    wallet_account_id: UUID
    bet_id: UUID
    amount: Money
    idempotency_key: str
    expires_at: datetime

    id: UUID = field(default_factory=uuid4)
    status: ReservationStatus = ReservationStatus.ACTIVE
    created_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None

    def settle(self) -> None:
        self._complete(ReservationStatus.SETTLED)

    def release(self) -> None:
        self._complete(ReservationStatus.RELEASED)

    def expire(self) -> None:
        self._complete(ReservationStatus.EXPIRED)

    def _complete(self, status: ReservationStatus) -> None:
        if self.status is not ReservationStatus.ACTIVE:
            raise ValueError("Reservation is already completed")

        self.status = status
        self.completed_at = utc_now()


@dataclass(frozen=True, slots=True, kw_only=True)
class LedgerEntry:
    wallet_account_id: UUID
    operation_id: UUID
    entry_type: LedgerEntryType
    direction: LedgerDirection
    amount: Money
    balance_after_minor: int
    reference_id: str

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
