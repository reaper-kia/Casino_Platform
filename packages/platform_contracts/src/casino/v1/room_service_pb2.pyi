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
    __slots__ = (
        "capacity",
        "closed_at",
        "created_at",
        "game_type",
        "is_system",
        "name",
        "owner_player_id",
        "participants_count",
        "revision",
        "room_id",
        "status",
        "updated_at",
        "visibility",
    )
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
    def __init__(
        self,
        room_id: str | None = ...,
        name: str | None = ...,
        game_type: _common_pb2.GameType | str | None = ...,
        visibility: RoomVisibility | str | None = ...,
        status: RoomStatus | str | None = ...,
        capacity: int | None = ...,
        participants_count: int | None = ...,
        revision: int | None = ...,
        owner_player_id: str | None = ...,
        is_system: bool | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        updated_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        closed_at: datetime.datetime | _timestamp_pb2.Timestamp | _Mapping | None = ...,
    ) -> None: ...

class RoomParticipantSnapshot(_message.Message):
    __slots__ = (
        "connection_status",
        "disconnected_at",
        "joined_at",
        "left_at",
        "membership_status",
        "participant_id",
        "player",
        "reconnect_deadline",
        "seat",
    )
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
    def __init__(
        self,
        participant_id: str | None = ...,
        player: _common_pb2.CasinoPlayerSummary | _Mapping | None = ...,
        seat: int | None = ...,
        membership_status: MembershipStatus | str | None = ...,
        connection_status: ConnectionStatus | str | None = ...,
        joined_at: datetime.datetime | _timestamp_pb2.Timestamp | _Mapping | None = ...,
        disconnected_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        reconnect_deadline: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        left_at: datetime.datetime | _timestamp_pb2.Timestamp | _Mapping | None = ...,
    ) -> None: ...

class RoomSnapshot(_message.Message):
    __slots__ = ("participants", "room", "server_time")
    ROOM_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    room: RoomSummary
    participants: _containers.RepeatedCompositeFieldContainer[RoomParticipantSnapshot]
    server_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        room: RoomSummary | _Mapping | None = ...,
        participants: _Iterable[RoomParticipantSnapshot | _Mapping] | None = ...,
        server_time: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class CreateRoomRequest(_message.Message):
    __slots__ = (
        "capacity",
        "context",
        "game_type",
        "idempotency_key",
        "name",
        "visibility",
    )
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
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        name: str | None = ...,
        game_type: _common_pb2.GameType | str | None = ...,
        visibility: RoomVisibility | str | None = ...,
        capacity: int | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class CreateRoomResponse(_message.Message):
    __slots__ = ("invite_token", "snapshot")
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    INVITE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    invite_token: str
    def __init__(
        self,
        snapshot: RoomSnapshot | _Mapping | None = ...,
        invite_token: str | None = ...,
    ) -> None: ...

class ListRoomsRequest(_message.Message):
    __slots__ = ("context", "cursor", "game_type", "limit", "status", "visibility")
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
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        game_type: _common_pb2.GameType | str | None = ...,
        visibility: RoomVisibility | str | None = ...,
        status: RoomStatus | str | None = ...,
        limit: int | None = ...,
        cursor: str | None = ...,
    ) -> None: ...

class ListRoomsResponse(_message.Message):
    __slots__ = ("next_cursor", "rooms")
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    rooms: _containers.RepeatedCompositeFieldContainer[RoomSummary]
    next_cursor: str
    def __init__(
        self,
        rooms: _Iterable[RoomSummary | _Mapping] | None = ...,
        next_cursor: str | None = ...,
    ) -> None: ...

class GetRoomSnapshotRequest(_message.Message):
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

class GetRoomSnapshotResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: RoomSnapshot | _Mapping | None = ...) -> None: ...

class JoinRoomRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "invite_token", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    INVITE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    invite_token: str
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
        invite_token: str | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class JoinRoomResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: RoomSnapshot | _Mapping | None = ...) -> None: ...

class LeaveRoomRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class LeaveRoomResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: RoomSnapshot | _Mapping | None = ...) -> None: ...

class CloseRoomRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class CloseRoomResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: RoomSnapshot | _Mapping | None = ...) -> None: ...

class MarkParticipantDisconnectedRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    idempotency_key: str
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
        idempotency_key: str | None = ...,
    ) -> None: ...

class MarkParticipantDisconnectedResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: RoomSnapshot | _Mapping | None = ...) -> None: ...

class ResumeRoomSessionRequest(_message.Message):
    __slots__ = ("context", "last_revision", "room_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_REVISION_FIELD_NUMBER: _ClassVar[int]
    context: _common_pb2.RequestContext
    room_id: str
    last_revision: int
    def __init__(
        self,
        context: _common_pb2.RequestContext | _Mapping | None = ...,
        room_id: str | None = ...,
        last_revision: int | None = ...,
    ) -> None: ...

class ResumeRoomSessionResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: RoomSnapshot
    def __init__(self, snapshot: RoomSnapshot | _Mapping | None = ...) -> None: ...
