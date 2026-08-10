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

class UserRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_ROLE_UNSPECIFIED: _ClassVar[UserRole]
    USER_ROLE_PLAYER: _ClassVar[UserRole]
    USER_ROLE_ADMIN: _ClassVar[UserRole]

class UserStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_STATUS_UNSPECIFIED: _ClassVar[UserStatus]
    USER_STATUS_ACTIVE: _ClassVar[UserStatus]
    USER_STATUS_BLOCKED: _ClassVar[UserStatus]
    USER_STATUS_DELETED: _ClassVar[UserStatus]

USER_ROLE_UNSPECIFIED: UserRole
USER_ROLE_PLAYER: UserRole
USER_ROLE_ADMIN: UserRole
USER_STATUS_UNSPECIFIED: UserStatus
USER_STATUS_ACTIVE: UserStatus
USER_STATUS_BLOCKED: UserStatus
USER_STATUS_DELETED: UserStatus

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

class UserSnapshot(_message.Message):
    __slots__ = (
        "created_at",
        "email",
        "nickname",
        "role",
        "status",
        "updated_at",
        "user_id",
    )
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    nickname: str
    role: UserRole
    status: UserStatus
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        user_id: str | None = ...,
        email: str | None = ...,
        nickname: str | None = ...,
        role: UserRole | str | None = ...,
        status: UserStatus | str | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        updated_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class TokenPair(_message.Message):
    __slots__ = (
        "access_token",
        "access_token_expires_at",
        "refresh_token",
        "refresh_token_expires_at",
    )
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    refresh_token: str
    access_token_expires_at: _timestamp_pb2.Timestamp
    refresh_token_expires_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        access_token: str | None = ...,
        refresh_token: str | None = ...,
        access_token_expires_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        refresh_token_expires_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ("context", "email", "nickname", "password")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    email: str
    nickname: str
    password: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        email: str | None = ...,
        nickname: str | None = ...,
        password: str | None = ...,
    ) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("tokens", "user")
    USER_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    user: UserSnapshot
    tokens: TokenPair
    def __init__(
        self,
        user: UserSnapshot | _Mapping | None = ...,
        tokens: TokenPair | _Mapping | None = ...,
    ) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("context", "email", "password")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    email: str
    password: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        email: str | None = ...,
        password: str | None = ...,
    ) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("tokens", "user")
    USER_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    user: UserSnapshot
    tokens: TokenPair
    def __init__(
        self,
        user: UserSnapshot | _Mapping | None = ...,
        tokens: TokenPair | _Mapping | None = ...,
    ) -> None: ...

class RefreshTokenRequest(_message.Message):
    __slots__ = ("context", "refresh_token")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    refresh_token: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        refresh_token: str | None = ...,
    ) -> None: ...

class RefreshTokenResponse(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: TokenPair
    def __init__(self, tokens: TokenPair | _Mapping | None = ...) -> None: ...

class LogoutRequest(_message.Message):
    __slots__ = ("all_sessions", "context", "refresh_token")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ALL_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    refresh_token: str
    all_sessions: bool
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        refresh_token: str | None = ...,
        all_sessions: bool | None = ...,
    ) -> None: ...

class LogoutResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMeRequest(_message.Message):
    __slots__ = ("context",)
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    def __init__(self, context: RequestContext | _Mapping | None = ...) -> None: ...

class GetMeResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: UserSnapshot
    def __init__(self, user: UserSnapshot | _Mapping | None = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("context", "user_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    user_id: str
    def __init__(
        self, context: RequestContext | _Mapping | None = ..., user_id: str | None = ...
    ) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: UserSnapshot
    def __init__(self, user: UserSnapshot | _Mapping | None = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ("context", "cursor", "limit", "role", "status")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    role: UserRole
    status: UserStatus
    limit: int
    cursor: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        role: UserRole | str | None = ...,
        status: UserStatus | str | None = ...,
        limit: int | None = ...,
        cursor: str | None = ...,
    ) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ("next_cursor", "users")
    USERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[UserSnapshot]
    next_cursor: str
    def __init__(
        self,
        users: _Iterable[UserSnapshot | _Mapping] | None = ...,
        next_cursor: str | None = ...,
    ) -> None: ...

class BlockUserRequest(_message.Message):
    __slots__ = ("context", "reason", "user_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    user_id: str
    reason: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        user_id: str | None = ...,
        reason: str | None = ...,
    ) -> None: ...

class BlockUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: UserSnapshot
    def __init__(self, user: UserSnapshot | _Mapping | None = ...) -> None: ...
