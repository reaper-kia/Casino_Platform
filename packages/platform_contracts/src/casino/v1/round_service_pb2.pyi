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
    __slots__ = ("server_seed_hash", "server_seed", "client_seed", "nonce", "algorithm_version")
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
    def __init__(self, server_seed_hash: _Optional[str] = ..., server_seed: _Optional[str] = ..., client_seed: _Optional[str] = ..., nonce: _Optional[int] = ..., algorithm_version: _Optional[str] = ...) -> None: ...

class RoundSummary(_message.Message):
    __slots__ = ("round_id", "room_id", "game_type", "round_number", "status", "revision", "configuration_version", "created_at", "betting_started_at", "started_at", "completed_at")
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
    def __init__(self, round_id: _Optional[str] = ..., room_id: _Optional[str] = ..., game_type: _Optional[_Union[_common_pb2.GameType, str]] = ..., round_number: _Optional[int] = ..., status: _Optional[_Union[RoundStatus, str]] = ..., revision: _Optional[int] = ..., configuration_version: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., betting_started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DiceRollResult(_message.Message):
    __slots__ = ("player_id", "values", "total")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    values: _containers.RepeatedScalarFieldContainer[int]
    total: int
    def __init__(self, player_id: _Optional[str] = ..., values: _Optional[_Iterable[int]] = ..., total: _Optional[int] = ...) -> None: ...

class DiceDuelResult(_message.Message):
    __slots__ = ("player_rolls", "winner_player_id")
    PLAYER_ROLLS_FIELD_NUMBER: _ClassVar[int]
    WINNER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_rolls: _containers.RepeatedCompositeFieldContainer[DiceRollResult]
    winner_player_id: str
    def __init__(self, player_rolls: _Optional[_Iterable[_Union[DiceRollResult, _Mapping]]] = ..., winner_player_id: _Optional[str] = ...) -> None: ...

class CrashResult(_message.Message):
    __slots__ = ("crash_multiplier_millis",)
    CRASH_MULTIPLIER_MILLIS_FIELD_NUMBER: _ClassVar[int]
    crash_multiplier_millis: int
    def __init__(self, crash_multiplier_millis: _Optional[int] = ...) -> None: ...

class RouletteResult(_message.Message):
    __slots__ = ("winning_pocket", "color")
    WINNING_POCKET_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    winning_pocket: str
    color: RouletteColor
    def __init__(self, winning_pocket: _Optional[str] = ..., color: _Optional[_Union[RouletteColor, str]] = ...) -> None: ...

class RoundSnapshot(_message.Message):
    __slots__ = ("round", "fairness", "dice_duel_result", "crash_result", "roulette_result")
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
    def __init__(self, round: _Optional[_Union[RoundSummary, _Mapping]] = ..., fairness: _Optional[_Union[FairnessPublicData, _Mapping]] = ..., dice_duel_result: _Optional[_Union[DiceDuelResult, _Mapping]] = ..., crash_result: _Optional[_Union[CrashResult, _Mapping]] = ..., roulette_result: _Optional[_Union[RouletteResult, _Mapping]] = ...) -> None: ...

class GetRoundRequest(_message.Message):
    __slots__ = ("context", "round_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., round_id: _Optional[str] = ...) -> None: ...

class GetRoundResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoundSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoundSnapshot, _Mapping]] = ...) -> None: ...

class GetCurrentRoundRequest(_message.Message):
    __slots__ = ("context", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ...) -> None: ...

class GetCurrentRoundResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoundSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoundSnapshot, _Mapping]] = ...) -> None: ...

class ListRoundsRequest(_message.Message):
    __slots__ = ("context", "room_id", "status", "limit", "cursor")
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
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ..., status: _Optional[_Union[RoundStatus, str]] = ..., limit: _Optional[int] = ..., cursor: _Optional[str] = ...) -> None: ...

class ListRoundsResponse(_message.Message):
    __slots__ = ("rounds", "next_cursor")
    ROUNDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    rounds: _containers.RepeatedCompositeFieldContainer[RoundSummary]
    next_cursor: str
    def __init__(self, rounds: _Optional[_Iterable[_Union[RoundSummary, _Mapping]]] = ..., next_cursor: _Optional[str] = ...) -> None: ...

class ReadyAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ThrowDiceAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CashOutAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SubmitRoundActionRequest(_message.Message):
    __slots__ = ("context", "round_id", "ready", "throw_dice", "cash_out", "expected_revision")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    THROW_DICE_FIELD_NUMBER: _ClassVar[int]
    CASH_OUT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    round_id: str
    ready: ReadyAction
    throw_dice: ThrowDiceAction
    cash_out: CashOutAction
    expected_revision: int
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., round_id: _Optional[str] = ..., ready: _Optional[_Union[ReadyAction, _Mapping]] = ..., throw_dice: _Optional[_Union[ThrowDiceAction, _Mapping]] = ..., cash_out: _Optional[_Union[CashOutAction, _Mapping]] = ..., expected_revision: _Optional[int] = ...) -> None: ...

class SubmitRoundActionResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoundSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoundSnapshot, _Mapping]] = ...) -> None: ...
