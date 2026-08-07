import datetime

from casino.v1 import common_pb2 as _common_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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
    def __init__(self, auto_cash_out_multiplier_millis: _Optional[int] = ...) -> None: ...

class RouletteBetSelection(_message.Message):
    __slots__ = ("bet_type", "pockets")
    BET_TYPE_FIELD_NUMBER: _ClassVar[int]
    POCKETS_FIELD_NUMBER: _ClassVar[int]
    bet_type: RouletteBetType
    pockets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, bet_type: _Optional[_Union[RouletteBetType, str]] = ..., pockets: _Optional[_Iterable[str]] = ...) -> None: ...

class BetSelection(_message.Message):
    __slots__ = ("dice_duel", "crash", "roulette")
    DICE_DUEL_FIELD_NUMBER: _ClassVar[int]
    CRASH_FIELD_NUMBER: _ClassVar[int]
    ROULETTE_FIELD_NUMBER: _ClassVar[int]
    dice_duel: DiceDuelBetSelection
    crash: CrashBetSelection
    roulette: RouletteBetSelection
    def __init__(self, dice_duel: _Optional[_Union[DiceDuelBetSelection, _Mapping]] = ..., crash: _Optional[_Union[CrashBetSelection, _Mapping]] = ..., roulette: _Optional[_Union[RouletteBetSelection, _Mapping]] = ...) -> None: ...

class BetSnapshot(_message.Message):
    __slots__ = ("bet_id", "round_id", "player_id", "amount", "selection", "status", "payout", "wallet_reservation_id", "created_at", "accepted_at", "settled_at")
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
    def __init__(self, bet_id: _Optional[str] = ..., round_id: _Optional[str] = ..., player_id: _Optional[str] = ..., amount: _Optional[_Union[_common_pb2.Money, _Mapping]] = ..., selection: _Optional[_Union[BetSelection, _Mapping]] = ..., status: _Optional[_Union[BetStatus, str]] = ..., payout: _Optional[_Union[_common_pb2.Money, _Mapping]] = ..., wallet_reservation_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., accepted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., settled_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PlaceBetRequest(_message.Message):
    __slots__ = ("context", "round_id", "amount", "selection")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    amount: _common_pb2.Money
    selection: BetSelection
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., round_id: _Optional[str] = ..., amount: _Optional[_Union[_common_pb2.Money, _Mapping]] = ..., selection: _Optional[_Union[BetSelection, _Mapping]] = ...) -> None: ...

class PlaceBetResponse(_message.Message):
    __slots__ = ("bet",)
    BET_FIELD_NUMBER: _ClassVar[int]
    bet: BetSnapshot
    def __init__(self, bet: _Optional[_Union[BetSnapshot, _Mapping]] = ...) -> None: ...

class CancelBetRequest(_message.Message):
    __slots__ = ("context", "bet_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    bet_id: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., bet_id: _Optional[str] = ...) -> None: ...

class CancelBetResponse(_message.Message):
    __slots__ = ("bet",)
    BET_FIELD_NUMBER: _ClassVar[int]
    bet: BetSnapshot
    def __init__(self, bet: _Optional[_Union[BetSnapshot, _Mapping]] = ...) -> None: ...

class GetBetRequest(_message.Message):
    __slots__ = ("context", "bet_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    bet_id: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., bet_id: _Optional[str] = ...) -> None: ...

class GetBetResponse(_message.Message):
    __slots__ = ("bet",)
    BET_FIELD_NUMBER: _ClassVar[int]
    bet: BetSnapshot
    def __init__(self, bet: _Optional[_Union[BetSnapshot, _Mapping]] = ...) -> None: ...

class ListMyBetsRequest(_message.Message):
    __slots__ = ("context", "round_id", "status", "limit", "cursor")
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
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., round_id: _Optional[str] = ..., status: _Optional[_Union[BetStatus, str]] = ..., limit: _Optional[int] = ..., cursor: _Optional[str] = ...) -> None: ...

class ListMyBetsResponse(_message.Message):
    __slots__ = ("bets", "next_cursor")
    BETS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    bets: _containers.RepeatedCompositeFieldContainer[BetSnapshot]
    next_cursor: str
    def __init__(self, bets: _Optional[_Iterable[_Union[BetSnapshot, _Mapping]]] = ..., next_cursor: _Optional[str] = ...) -> None: ...
