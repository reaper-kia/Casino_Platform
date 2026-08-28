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

class RoundStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROUND_STATUS_UNSPECIFIED: _ClassVar[RoundStatus]
    ROUND_STATUS_SCHEDULED: _ClassVar[RoundStatus]
    ROUND_STATUS_BETTING: _ClassVar[RoundStatus]
    ROUND_STATUS_LOCKED: _ClassVar[RoundStatus]
    ROUND_STATUS_RUNNING: _ClassVar[RoundStatus]
    ROUND_STATUS_SETTLEMENT_PENDING: _ClassVar[RoundStatus]
    ROUND_STATUS_COMPLETED: _ClassVar[RoundStatus]
    ROUND_STATUS_CANCELLED: _ClassVar[RoundStatus]

class RouletteColor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROULETTE_COLOR_UNSPECIFIED: _ClassVar[RouletteColor]
    ROULETTE_COLOR_RED: _ClassVar[RouletteColor]
    ROULETTE_COLOR_BLACK: _ClassVar[RouletteColor]
    ROULETTE_COLOR_GREEN: _ClassVar[RouletteColor]

ROUND_STATUS_UNSPECIFIED: RoundStatus
ROUND_STATUS_SCHEDULED: RoundStatus
ROUND_STATUS_BETTING: RoundStatus
ROUND_STATUS_LOCKED: RoundStatus
ROUND_STATUS_RUNNING: RoundStatus
ROUND_STATUS_SETTLEMENT_PENDING: RoundStatus
ROUND_STATUS_COMPLETED: RoundStatus
ROUND_STATUS_CANCELLED: RoundStatus
ROULETTE_COLOR_UNSPECIFIED: RouletteColor
ROULETTE_COLOR_RED: RouletteColor
ROULETTE_COLOR_BLACK: RouletteColor
ROULETTE_COLOR_GREEN: RouletteColor

class FairnessPublicData(_message.Message):
    __slots__ = (
        "algorithm_version",
        "client_seed",
        "nonce",
        "server_seed",
        "server_seed_hash",
    )
    SERVER_SEED_HASH_FIELD_NUMBER: _ClassVar[int]
    SERVER_SEED_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SEED_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_VERSION_FIELD_NUMBER: _ClassVar[int]
    server_seed_hash: str
    server_seed: str
    client_seed: str
    nonce: int
    algorithm_version: str
    def __init__(
        self,
        server_seed_hash: str | None = ...,
        server_seed: str | None = ...,
        client_seed: str | None = ...,
        nonce: int | None = ...,
        algorithm_version: str | None = ...,
    ) -> None: ...

class RoundSummary(_message.Message):
    __slots__ = (
        "betting_started_at",
        "completed_at",
        "configuration_version",
        "created_at",
        "game_type",
        "revision",
        "room_id",
        "round_id",
        "round_number",
        "started_at",
        "status",
    )
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROUND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    BETTING_STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    round_id: str
    room_id: str
    game_type: _common_pb2.GameType
    round_number: int
    status: RoundStatus
    revision: int
    configuration_version: str
    created_at: _timestamp_pb2.Timestamp
    betting_started_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        round_id: str | None = ...,
        room_id: str | None = ...,
        game_type: _common_pb2.GameType | str | None = ...,
        round_number: int | None = ...,
        status: RoundStatus | str | None = ...,
        revision: int | None = ...,
        configuration_version: str | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        betting_started_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        started_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        completed_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class DiceRollResult(_message.Message):
    __slots__ = ("player_id", "total", "values")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    values: _containers.RepeatedScalarFieldContainer[int]
    total: int
    def __init__(
        self,
        player_id: str | None = ...,
        values: _Iterable[int] | None = ...,
        total: int | None = ...,
    ) -> None: ...

class DiceDuelResult(_message.Message):
    __slots__ = ("player_rolls", "winner_player_id")
    PLAYER_ROLLS_FIELD_NUMBER: _ClassVar[int]
    WINNER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_rolls: _containers.RepeatedCompositeFieldContainer[DiceRollResult]
    winner_player_id: str
    def __init__(
        self,
        player_rolls: _Iterable[DiceRollResult | _Mapping] | None = ...,
        winner_player_id: str | None = ...,
    ) -> None: ...

class CrashResult(_message.Message):
    __slots__ = ("crash_multiplier_millis",)
    CRASH_MULTIPLIER_MILLIS_FIELD_NUMBER: _ClassVar[int]
    crash_multiplier_millis: int
    def __init__(self, crash_multiplier_millis: int | None = ...) -> None: ...

class RouletteResult(_message.Message):
    __slots__ = ("color", "winning_pocket")
    WINNING_POCKET_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    winning_pocket: str
    color: RouletteColor
    def __init__(
        self, winning_pocket: str | None = ..., color: RouletteColor | str | None = ...
    ) -> None: ...

class RoundSnapshot(_message.Message):
    __slots__ = (
        "crash_result",
        "dice_duel_result",
        "fairness",
        "roulette_result",
        "round",
    )
    ROUND_FIELD_NUMBER: _ClassVar[int]
    FAIRNESS_FIELD_NUMBER: _ClassVar[int]
    DICE_DUEL_RESULT_FIELD_NUMBER: _ClassVar[int]
    CRASH_RESULT_FIELD_NUMBER: _ClassVar[int]
    ROULETTE_RESULT_FIELD_NUMBER: _ClassVar[int]
    round: RoundSummary
    fairness: FairnessPublicData
    dice_duel_result: DiceDuelResult
    crash_result: CrashResult
    roulette_result: RouletteResult
    def __init__(
        self,
        round: RoundSummary | _Mapping | None = ...,
        fairness: FairnessPublicData | _Mapping | None = ...,
        dice_duel_result: DiceDuelResult | _Mapping | None = ...,
        crash_result: CrashResult | _Mapping | None = ...,
        roulette_result: RouletteResult | _Mapping | None = ...,
    ) -> None: ...

class GetRoundRequest(_message.Message):
    __slots__ = ("context", "round_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        round_id: str | None = ...,
    ) -> None: ...

class GetRoundResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoundSnapshot
    def __init__(self, snapshot: RoundSnapshot | _Mapping | None = ...) -> None: ...

class GetCurrentRoundRequest(_message.Message):
    __slots__ = ("context", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
    ) -> None: ...

class GetCurrentRoundResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoundSnapshot
    def __init__(self, snapshot: RoundSnapshot | _Mapping | None = ...) -> None: ...

class ListRoundsRequest(_message.Message):
    __slots__ = ("context", "cursor", "limit", "room_id", "status")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    status: RoundStatus
    limit: int
    cursor: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
        status: RoundStatus | str | None = ...,
        limit: int | None = ...,
        cursor: str | None = ...,
    ) -> None: ...

class ListRoundsResponse(_message.Message):
    __slots__ = ("next_cursor", "rounds")
    ROUNDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    rounds: _containers.RepeatedCompositeFieldContainer[RoundSummary]
    next_cursor: str
    def __init__(
        self,
        rounds: _Iterable[RoundSummary | _Mapping] | None = ...,
        next_cursor: str | None = ...,
    ) -> None: ...

class ReadyAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ThrowDiceAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CashOutAction(_message.Message):
    __slots__ = ("bet_id",)
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    bet_id: str
    def __init__(self, bet_id: str | None = ...) -> None: ...

class SubmitRoundActionRequest(_message.Message):
    __slots__ = (
        "cash_out",
        "context",
        "expected_revision",
        "idempotency_key",
        "ready",
        "round_id",
        "throw_dice",
    )
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    THROW_DICE_FIELD_NUMBER: _ClassVar[int]
    CASH_OUT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    ready: ReadyAction
    throw_dice: ThrowDiceAction
    cash_out: CashOutAction
    expected_revision: int
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        round_id: str | None = ...,
        ready: ReadyAction | _Mapping | None = ...,
        throw_dice: ThrowDiceAction | _Mapping | None = ...,
        cash_out: CashOutAction | _Mapping | None = ...,
        expected_revision: int | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class SubmitRoundActionResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoundSnapshot
    def __init__(self, snapshot: RoundSnapshot | _Mapping | None = ...) -> None: ...
