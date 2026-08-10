import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from casino.v1 import common_pb2 as _common_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class BetStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BET_STATUS_UNSPECIFIED: _ClassVar[BetStatus]
    BET_STATUS_PENDING_RESERVATION: _ClassVar[BetStatus]
    BET_STATUS_ACCEPTED: _ClassVar[BetStatus]
    BET_STATUS_REJECTED: _ClassVar[BetStatus]
    BET_STATUS_SETTLEMENT_PENDING: _ClassVar[BetStatus]
    BET_STATUS_SETTLED: _ClassVar[BetStatus]
    BET_STATUS_CANCELLED: _ClassVar[BetStatus]

class RouletteBetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROULETTE_BET_TYPE_UNSPECIFIED: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_STRAIGHT: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_SPLIT: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_STREET: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_CORNER: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_LINE: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_DOZEN: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_COLUMN: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_RED: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_BLACK: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_EVEN: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_ODD: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_LOW: _ClassVar[RouletteBetType]
    ROULETTE_BET_TYPE_HIGH: _ClassVar[RouletteBetType]

BET_STATUS_UNSPECIFIED: BetStatus
BET_STATUS_PENDING_RESERVATION: BetStatus
BET_STATUS_ACCEPTED: BetStatus
BET_STATUS_REJECTED: BetStatus
BET_STATUS_SETTLEMENT_PENDING: BetStatus
BET_STATUS_SETTLED: BetStatus
BET_STATUS_CANCELLED: BetStatus
ROULETTE_BET_TYPE_UNSPECIFIED: RouletteBetType
ROULETTE_BET_TYPE_STRAIGHT: RouletteBetType
ROULETTE_BET_TYPE_SPLIT: RouletteBetType
ROULETTE_BET_TYPE_STREET: RouletteBetType
ROULETTE_BET_TYPE_CORNER: RouletteBetType
ROULETTE_BET_TYPE_LINE: RouletteBetType
ROULETTE_BET_TYPE_DOZEN: RouletteBetType
ROULETTE_BET_TYPE_COLUMN: RouletteBetType
ROULETTE_BET_TYPE_RED: RouletteBetType
ROULETTE_BET_TYPE_BLACK: RouletteBetType
ROULETTE_BET_TYPE_EVEN: RouletteBetType
ROULETTE_BET_TYPE_ODD: RouletteBetType
ROULETTE_BET_TYPE_LOW: RouletteBetType
ROULETTE_BET_TYPE_HIGH: RouletteBetType

class DiceDuelBetSelection(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CrashBetSelection(_message.Message):
    __slots__ = ("auto_cash_out_multiplier_millis",)
    AUTO_CASH_OUT_MULTIPLIER_MILLIS_FIELD_NUMBER: _ClassVar[int]
    auto_cash_out_multiplier_millis: int
    def __init__(self, auto_cash_out_multiplier_millis: int | None = ...) -> None: ...

class RouletteBetSelection(_message.Message):
    __slots__ = ("bet_type", "pockets")
    BET_TYPE_FIELD_NUMBER: _ClassVar[int]
    POCKETS_FIELD_NUMBER: _ClassVar[int]
    bet_type: RouletteBetType
    pockets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        bet_type: RouletteBetType | str | None = ...,
        pockets: _Iterable[str] | None = ...,
    ) -> None: ...

class BetSelection(_message.Message):
    __slots__ = ("crash", "dice_duel", "roulette")
    DICE_DUEL_FIELD_NUMBER: _ClassVar[int]
    CRASH_FIELD_NUMBER: _ClassVar[int]
    ROULETTE_FIELD_NUMBER: _ClassVar[int]
    dice_duel: DiceDuelBetSelection
    crash: CrashBetSelection
    roulette: RouletteBetSelection
    def __init__(
        self,
        dice_duel: DiceDuelBetSelection | _Mapping | None = ...,
        crash: CrashBetSelection | _Mapping | None = ...,
        roulette: RouletteBetSelection | _Mapping | None = ...,
    ) -> None: ...

class BetSnapshot(_message.Message):
    __slots__ = (
        "accepted_at",
        "amount",
        "bet_id",
        "created_at",
        "payout",
        "player_id",
        "round_id",
        "selection",
        "settled_at",
        "status",
        "wallet_reservation_id",
    )
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAYOUT_FIELD_NUMBER: _ClassVar[int]
    WALLET_RESERVATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    SETTLED_AT_FIELD_NUMBER: _ClassVar[int]
    bet_id: str
    round_id: str
    player_id: str
    amount: _common_pb2.Money
    selection: BetSelection
    status: BetStatus
    payout: _common_pb2.Money
    wallet_reservation_id: str
    created_at: _timestamp_pb2.Timestamp
    accepted_at: _timestamp_pb2.Timestamp
    settled_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        bet_id: str | None = ...,
        round_id: str | None = ...,
        player_id: str | None = ...,
        amount: _common_pb2.Money | _Mapping | None = ...,
        selection: BetSelection | _Mapping | None = ...,
        status: BetStatus | str | None = ...,
        payout: _common_pb2.Money | _Mapping | None = ...,
        wallet_reservation_id: str | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        accepted_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        settled_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class PlaceBetRequest(_message.Message):
    __slots__ = ("amount", "context", "idempotency_key", "round_id", "selection")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    amount: _common_pb2.Money
    selection: BetSelection
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        round_id: str | None = ...,
        amount: _common_pb2.Money | _Mapping | None = ...,
        selection: BetSelection | _Mapping | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class PlaceBetResponse(_message.Message):
    __slots__ = ("bet",)
    BET_FIELD_NUMBER: _ClassVar[int]
    bet: BetSnapshot
    def __init__(self, bet: BetSnapshot | _Mapping | None = ...) -> None: ...

class CancelBetRequest(_message.Message):
    __slots__ = ("bet_id", "context", "idempotency_key")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    bet_id: str
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        bet_id: str | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class CancelBetResponse(_message.Message):
    __slots__ = ("bet",)
    BET_FIELD_NUMBER: _ClassVar[int]
    bet: BetSnapshot
    def __init__(self, bet: BetSnapshot | _Mapping | None = ...) -> None: ...

class GetBetRequest(_message.Message):
    __slots__ = ("bet_id", "context")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    bet_id: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        bet_id: str | None = ...,
    ) -> None: ...

class GetBetResponse(_message.Message):
    __slots__ = ("bet",)
    BET_FIELD_NUMBER: _ClassVar[int]
    bet: BetSnapshot
    def __init__(self, bet: BetSnapshot | _Mapping | None = ...) -> None: ...

class ListMyBetsRequest(_message.Message):
    __slots__ = ("context", "cursor", "limit", "round_id", "status")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    status: BetStatus
    limit: int
    cursor: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        round_id: str | None = ...,
        status: BetStatus | str | None = ...,
        limit: int | None = ...,
        cursor: str | None = ...,
    ) -> None: ...

class ListMyBetsResponse(_message.Message):
    __slots__ = ("bets", "next_cursor")
    BETS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    bets: _containers.RepeatedCompositeFieldContainer[BetSnapshot]
    next_cursor: str
    def __init__(
        self,
        bets: _Iterable[BetSnapshot | _Mapping] | None = ...,
        next_cursor: str | None = ...,
    ) -> None: ...
