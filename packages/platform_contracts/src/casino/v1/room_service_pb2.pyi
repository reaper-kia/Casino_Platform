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

class RoomVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROOM_VISIBILITY_UNSPECIFIED: _ClassVar[RoomVisibility]
    ROOM_VISIBILITY_PUBLIC: _ClassVar[RoomVisibility]
    ROOM_VISIBILITY_PRIVATE: _ClassVar[RoomVisibility]

class RoomStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROOM_STATUS_UNSPECIFIED: _ClassVar[RoomStatus]
    ROOM_STATUS_OPEN: _ClassVar[RoomStatus]
    ROOM_STATUS_CLOSED: _ClassVar[RoomStatus]
    ROOM_STATUS_ARCHIVED: _ClassVar[RoomStatus]

class MembershipStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBERSHIP_STATUS_UNSPECIFIED: _ClassVar[MembershipStatus]
    MEMBERSHIP_STATUS_ACTIVE: _ClassVar[MembershipStatus]
    MEMBERSHIP_STATUS_LEFT: _ClassVar[MembershipStatus]

class ConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_STATUS_UNSPECIFIED: _ClassVar[ConnectionStatus]
    CONNECTION_STATUS_CONNECTED: _ClassVar[ConnectionStatus]
    CONNECTION_STATUS_DISCONNECTED: _ClassVar[ConnectionStatus]
ROOM_VISIBILITY_UNSPECIFIED: RoomVisibility
ROOM_VISIBILITY_PUBLIC: RoomVisibility
ROOM_VISIBILITY_PRIVATE: RoomVisibility
ROOM_STATUS_UNSPECIFIED: RoomStatus
ROOM_STATUS_OPEN: RoomStatus
ROOM_STATUS_CLOSED: RoomStatus
ROOM_STATUS_ARCHIVED: RoomStatus
MEMBERSHIP_STATUS_UNSPECIFIED: MembershipStatus
MEMBERSHIP_STATUS_ACTIVE: MembershipStatus
MEMBERSHIP_STATUS_LEFT: MembershipStatus
CONNECTION_STATUS_UNSPECIFIED: ConnectionStatus
CONNECTION_STATUS_CONNECTED: ConnectionStatus
CONNECTION_STATUS_DISCONNECTED: ConnectionStatus

class RoomSummary(_message.Message):
    __slots__ = ("room_id", "name", "game_type", "visibility", "status", "capacity", "participants_count", "revision", "owner_player_id", "is_system", "created_at", "updated_at", "closed_at")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    OWNER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    IS_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_AT_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    name: str
    game_type: _common_pb2.GameType
    visibility: RoomVisibility
    status: RoomStatus
    capacity: int
    participants_count: int
    revision: int
    owner_player_id: str
    is_system: bool
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    closed_at: _timestamp_pb2.Timestamp
    def __init__(self, room_id: _Optional[str] = ..., name: _Optional[str] = ..., game_type: _Optional[_Union[_common_pb2.GameType, str]] = ..., visibility: _Optional[_Union[RoomVisibility, str]] = ..., status: _Optional[_Union[RoomStatus, str]] = ..., capacity: _Optional[int] = ..., participants_count: _Optional[int] = ..., revision: _Optional[int] = ..., owner_player_id: _Optional[str] = ..., is_system: _Optional[bool] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., closed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RoomParticipantSnapshot(_message.Message):
    __slots__ = ("participant_id", "player", "seat", "membership_status", "connection_status", "joined_at", "disconnected_at", "reconnect_deadline", "left_at")
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    JOINED_AT_FIELD_NUMBER: _ClassVar[int]
    DISCONNECTED_AT_FIELD_NUMBER: _ClassVar[int]
    RECONNECT_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    LEFT_AT_FIELD_NUMBER: _ClassVar[int]
    participant_id: str
    player: _common_pb2.CasinoPlayerSummary
    seat: int
    membership_status: MembershipStatus
    connection_status: ConnectionStatus
    joined_at: _timestamp_pb2.Timestamp
    disconnected_at: _timestamp_pb2.Timestamp
    reconnect_deadline: _timestamp_pb2.Timestamp
    left_at: _timestamp_pb2.Timestamp
    def __init__(self, participant_id: _Optional[str] = ..., player: _Optional[_Union[_common_pb2.CasinoPlayerSummary, _Mapping]] = ..., seat: _Optional[int] = ..., membership_status: _Optional[_Union[MembershipStatus, str]] = ..., connection_status: _Optional[_Union[ConnectionStatus, str]] = ..., joined_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., disconnected_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., reconnect_deadline: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., left_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RoomSnapshot(_message.Message):
    __slots__ = ("room", "participants", "server_time")
    ROOM_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    room: RoomSummary
    participants: _containers.RepeatedCompositeFieldContainer[RoomParticipantSnapshot]
    server_time: _timestamp_pb2.Timestamp
    def __init__(self, room: _Optional[_Union[RoomSummary, _Mapping]] = ..., participants: _Optional[_Iterable[_Union[RoomParticipantSnapshot, _Mapping]]] = ..., server_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateRoomRequest(_message.Message):
    __slots__ = ("context", "name", "game_type", "visibility", "capacity", "idempotency_key")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    name: str
    game_type: _common_pb2.GameType
    visibility: RoomVisibility
    capacity: int
    idempotency_key: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., name: _Optional[str] = ..., game_type: _Optional[_Union[_common_pb2.GameType, str]] = ..., visibility: _Optional[_Union[RoomVisibility, str]] = ..., capacity: _Optional[int] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class CreateRoomResponse(_message.Message):
    __slots__ = ("snapshot", "invite_token")
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    INVITE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    invite_token: str
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ..., invite_token: _Optional[str] = ...) -> None: ...

class ListRoomsRequest(_message.Message):
    __slots__ = ("context", "game_type", "visibility", "status", "limit", "cursor")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    game_type: _common_pb2.GameType
    visibility: RoomVisibility
    status: RoomStatus
    limit: int
    cursor: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., game_type: _Optional[_Union[_common_pb2.GameType, str]] = ..., visibility: _Optional[_Union[RoomVisibility, str]] = ..., status: _Optional[_Union[RoomStatus, str]] = ..., limit: _Optional[int] = ..., cursor: _Optional[str] = ...) -> None: ...

class ListRoomsResponse(_message.Message):
    __slots__ = ("rooms", "next_cursor")
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    rooms: _containers.RepeatedCompositeFieldContainer[RoomSummary]
    next_cursor: str
    def __init__(self, rooms: _Optional[_Iterable[_Union[RoomSummary, _Mapping]]] = ..., next_cursor: _Optional[str] = ...) -> None: ...

class GetRoomSnapshotRequest(_message.Message):
    __slots__ = ("context", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ...) -> None: ...

class GetRoomSnapshotResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ...) -> None: ...

class JoinRoomRequest(_message.Message):
    __slots__ = ("context", "room_id", "invite_token", "idempotency_key")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    INVITE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    invite_token: str
    idempotency_key: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ..., invite_token: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class JoinRoomResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ...) -> None: ...

class LeaveRoomRequest(_message.Message):
    __slots__ = ("context", "room_id", "idempotency_key")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    idempotency_key: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class LeaveRoomResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ...) -> None: ...

class CloseRoomRequest(_message.Message):
    __slots__ = ("context", "room_id", "idempotency_key")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    idempotency_key: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class CloseRoomResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ...) -> None: ...

class MarkParticipantDisconnectedRequest(_message.Message):
    __slots__ = ("context", "room_id", "idempotency_key")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    idempotency_key: str
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class MarkParticipantDisconnectedResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ...) -> None: ...

class ResumeRoomSessionRequest(_message.Message):
    __slots__ = ("context", "room_id", "last_revision")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_REVISION_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    last_revision: int
    def __init__(self, context: _Optional[_Union[_common_pb2.RequestContext, _Mapping]] = ..., room_id: _Optional[str] = ..., last_revision: _Optional[int] = ...) -> None: ...

class ResumeRoomSessionResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: _Optional[_Union[RoomSnapshot, _Mapping]] = ...) -> None: ...
