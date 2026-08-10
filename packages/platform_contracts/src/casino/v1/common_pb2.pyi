import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class GameType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GAME_TYPE_UNSPECIFIED: _ClassVar[GameType]
    GAME_TYPE_DICE_DUEL: _ClassVar[GameType]
    GAME_TYPE_CRASH: _ClassVar[GameType]
    GAME_TYPE_ROULETTE: _ClassVar[GameType]

class CasinoPlayerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CASINO_PLAYER_STATUS_UNSPECIFIED: _ClassVar[CasinoPlayerStatus]
    CASINO_PLAYER_STATUS_ACTIVE: _ClassVar[CasinoPlayerStatus]
    CASINO_PLAYER_STATUS_BLOCKED: _ClassVar[CasinoPlayerStatus]

GAME_TYPE_UNSPECIFIED: GameType
GAME_TYPE_DICE_DUEL: GameType
GAME_TYPE_CRASH: GameType
GAME_TYPE_ROULETTE: GameType
CASINO_PLAYER_STATUS_UNSPECIFIED: CasinoPlayerStatus
CASINO_PLAYER_STATUS_ACTIVE: CasinoPlayerStatus
CASINO_PLAYER_STATUS_BLOCKED: CasinoPlayerStatus

class RequestContext(_message.Message):
    __slots__ = ("actor_identity_user_id", "permissions", "request_id")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    actor_identity_user_id: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        request_id: str | None = ...,
        actor_identity_user_id: str | None = ...,
        permissions: _Iterable[str] | None = ...,
    ) -> None: ...

class Money(_message.Message):
    __slots__ = ("amount_minor", "currency")
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    amount_minor: int
    currency: str
    def __init__(
        self, amount_minor: int | None = ..., currency: str | None = ...
    ) -> None: ...

class CasinoPlayerSummary(_message.Message):
    __slots__ = (
        "avatar_url",
        "identity_user_id",
        "nickname",
        "player_id",
        "status",
        "updated_at",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    identity_user_id: str
    nickname: str
    avatar_url: str
    status: CasinoPlayerStatus
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        player_id: str | None = ...,
        identity_user_id: str | None = ...,
        nickname: str | None = ...,
        avatar_url: str | None = ...,
        status: CasinoPlayerStatus | str | None = ...,
        updated_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...
