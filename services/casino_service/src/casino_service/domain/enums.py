from enum import StrEnum


class GameType(StrEnum):
    DICE_DUEL = "dice_duel"
    CRASH = "crash"
    ROULETTE = "roulette"
    POKER = "poker"


class CasinoPlayerStatus(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class RoomVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class RoomStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"


class MembershipStatus(StrEnum):
    ACTIVE = "active"
    LEFT = "left"


class ConnectionStatus(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class RoundStatus(StrEnum):
    SCHEDULED = "scheduled"
    BETTING = "betting"
    LOCKED = "locked"
    RUNNING = "running"
    SETTLEMENT_PENDING = "settlement_pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BetStatus(StrEnum):
    PENDING_RESERVATION = "pending_reservation"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SETTLEMENT_PENDING = "settlement_pending"
    SETTLED = "settled"
    CANCELLED = "cancelled"


class RoundActionType(StrEnum):
    READY = "ready"
    THROW = "throw"
    CASH_OUT = "cash_out"