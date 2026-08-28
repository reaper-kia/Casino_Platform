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

class WalletStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WALLET_STATUS_UNSPECIFIED: _ClassVar[WalletStatus]
    WALLET_STATUS_ACTIVE: _ClassVar[WalletStatus]
    WALLET_STATUS_FROZEN: _ClassVar[WalletStatus]
    WALLET_STATUS_CLOSED: _ClassVar[WalletStatus]

class ReservationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESERVATION_STATUS_UNSPECIFIED: _ClassVar[ReservationStatus]
    RESERVATION_STATUS_ACTIVE: _ClassVar[ReservationStatus]
    RESERVATION_STATUS_SETTLED: _ClassVar[ReservationStatus]
    RESERVATION_STATUS_RELEASED: _ClassVar[ReservationStatus]
    RESERVATION_STATUS_EXPIRED: _ClassVar[ReservationStatus]

class LedgerDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEDGER_DIRECTION_UNSPECIFIED: _ClassVar[LedgerDirection]
    LEDGER_DIRECTION_CREDIT: _ClassVar[LedgerDirection]
    LEDGER_DIRECTION_DEBIT: _ClassVar[LedgerDirection]

class LedgerEntryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEDGER_ENTRY_TYPE_UNSPECIFIED: _ClassVar[LedgerEntryType]
    LEDGER_ENTRY_TYPE_INITIAL_GRANT: _ClassVar[LedgerEntryType]
    LEDGER_ENTRY_TYPE_BET_SETTLEMENT: _ClassVar[LedgerEntryType]
    LEDGER_ENTRY_TYPE_BONUS: _ClassVar[LedgerEntryType]
    LEDGER_ENTRY_TYPE_ADMIN_ADJUSTMENT: _ClassVar[LedgerEntryType]

WALLET_STATUS_UNSPECIFIED: WalletStatus
WALLET_STATUS_ACTIVE: WalletStatus
WALLET_STATUS_FROZEN: WalletStatus
WALLET_STATUS_CLOSED: WalletStatus
RESERVATION_STATUS_UNSPECIFIED: ReservationStatus
RESERVATION_STATUS_ACTIVE: ReservationStatus
RESERVATION_STATUS_SETTLED: ReservationStatus
RESERVATION_STATUS_RELEASED: ReservationStatus
RESERVATION_STATUS_EXPIRED: ReservationStatus
LEDGER_DIRECTION_UNSPECIFIED: LedgerDirection
LEDGER_DIRECTION_CREDIT: LedgerDirection
LEDGER_DIRECTION_DEBIT: LedgerDirection
LEDGER_ENTRY_TYPE_UNSPECIFIED: LedgerEntryType
LEDGER_ENTRY_TYPE_INITIAL_GRANT: LedgerEntryType
LEDGER_ENTRY_TYPE_BET_SETTLEMENT: LedgerEntryType
LEDGER_ENTRY_TYPE_BONUS: LedgerEntryType
LEDGER_ENTRY_TYPE_ADMIN_ADJUSTMENT: LedgerEntryType

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

class WalletSnapshot(_message.Message):
    __slots__ = (
        "accounting_balance",
        "available_balance",
        "created_at",
        "identity_user_id",
        "reserved_amount",
        "status",
        "updated_at",
        "version",
        "wallet_account_id",
    )
    WALLET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTING_BALANCE_FIELD_NUMBER: _ClassVar[int]
    RESERVED_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    wallet_account_id: str
    identity_user_id: str
    accounting_balance: Money
    reserved_amount: Money
    available_balance: Money
    status: WalletStatus
    version: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        wallet_account_id: str | None = ...,
        identity_user_id: str | None = ...,
        accounting_balance: Money | _Mapping | None = ...,
        reserved_amount: Money | _Mapping | None = ...,
        available_balance: Money | _Mapping | None = ...,
        status: WalletStatus | str | None = ...,
        version: int | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        updated_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class ReservationSnapshot(_message.Message):
    __slots__ = (
        "amount",
        "bet_id",
        "completed_at",
        "created_at",
        "expires_at",
        "reservation_id",
        "status",
        "wallet_account_id",
    )
    RESERVATION_ID_FIELD_NUMBER: _ClassVar[int]
    WALLET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    reservation_id: str
    wallet_account_id: str
    bet_id: str
    amount: Money
    status: ReservationStatus
    expires_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        reservation_id: str | None = ...,
        wallet_account_id: str | None = ...,
        bet_id: str | None = ...,
        amount: Money | _Mapping | None = ...,
        status: ReservationStatus | str | None = ...,
        expires_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
        completed_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class LedgerEntrySnapshot(_message.Message):
    __slots__ = (
        "amount",
        "balance_after",
        "created_at",
        "direction",
        "entry_type",
        "ledger_entry_id",
        "operation_id",
        "reference_id",
        "wallet_account_id",
    )
    LEDGER_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    WALLET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_AFTER_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ledger_entry_id: str
    wallet_account_id: str
    operation_id: str
    entry_type: LedgerEntryType
    direction: LedgerDirection
    amount: Money
    balance_after: Money
    reference_id: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        ledger_entry_id: str | None = ...,
        wallet_account_id: str | None = ...,
        operation_id: str | None = ...,
        entry_type: LedgerEntryType | str | None = ...,
        direction: LedgerDirection | str | None = ...,
        amount: Money | _Mapping | None = ...,
        balance_after: Money | _Mapping | None = ...,
        reference_id: str | None = ...,
        created_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class GetWalletRequest(_message.Message):
    __slots__ = ("context", "identity_user_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    identity_user_id: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        identity_user_id: str | None = ...,
    ) -> None: ...

class GetWalletResponse(_message.Message):
    __slots__ = ("wallet",)
    WALLET_FIELD_NUMBER: _ClassVar[int]
    wallet: WalletSnapshot
    def __init__(self, wallet: WalletSnapshot | _Mapping | None = ...) -> None: ...

class ListLedgerEntriesRequest(_message.Message):
    __slots__ = (
        "context",
        "cursor",
        "direction",
        "entry_type",
        "identity_user_id",
        "limit",
    )
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    identity_user_id: str
    entry_type: LedgerEntryType
    direction: LedgerDirection
    limit: int
    cursor: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        identity_user_id: str | None = ...,
        entry_type: LedgerEntryType | str | None = ...,
        direction: LedgerDirection | str | None = ...,
        limit: int | None = ...,
        cursor: str | None = ...,
    ) -> None: ...

class ListLedgerEntriesResponse(_message.Message):
    __slots__ = ("entries", "next_cursor")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[LedgerEntrySnapshot]
    next_cursor: str
    def __init__(
        self,
        entries: _Iterable[LedgerEntrySnapshot | _Mapping] | None = ...,
        next_cursor: str | None = ...,
    ) -> None: ...

class ReserveFundsRequest(_message.Message):
    __slots__ = (
        "amount",
        "bet_id",
        "context",
        "expires_at",
        "idempotency_key",
        "identity_user_id",
    )
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    idempotency_key: str
    identity_user_id: str
    bet_id: str
    amount: Money
    expires_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        idempotency_key: str | None = ...,
        identity_user_id: str | None = ...,
        bet_id: str | None = ...,
        amount: Money | _Mapping | None = ...,
        expires_at: datetime.datetime
        | _timestamp_pb2.Timestamp
        | _Mapping
        | None = ...,
    ) -> None: ...

class ReserveFundsResponse(_message.Message):
    __slots__ = ("reservation", "wallet")
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    WALLET_FIELD_NUMBER: _ClassVar[int]
    reservation: ReservationSnapshot
    wallet: WalletSnapshot
    def __init__(
        self,
        reservation: ReservationSnapshot | _Mapping | None = ...,
        wallet: WalletSnapshot | _Mapping | None = ...,
    ) -> None: ...

class SettleBetRequest(_message.Message):
    __slots__ = ("bet_id", "context", "idempotency_key", "payout", "reservation_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_ID_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    PAYOUT_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    idempotency_key: str
    reservation_id: str
    bet_id: str
    payout: Money
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        idempotency_key: str | None = ...,
        reservation_id: str | None = ...,
        bet_id: str | None = ...,
        payout: Money | _Mapping | None = ...,
    ) -> None: ...

class SettleBetResponse(_message.Message):
    __slots__ = ("ledger_entries", "reservation", "wallet")
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    WALLET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    reservation: ReservationSnapshot
    wallet: WalletSnapshot
    ledger_entries: _containers.RepeatedCompositeFieldContainer[LedgerEntrySnapshot]
    def __init__(
        self,
        reservation: ReservationSnapshot | _Mapping | None = ...,
        wallet: WalletSnapshot | _Mapping | None = ...,
        ledger_entries: _Iterable[LedgerEntrySnapshot | _Mapping] | None = ...,
    ) -> None: ...

class ReleaseReservationRequest(_message.Message):
    __slots__ = ("bet_id", "context", "idempotency_key", "reason", "reservation_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_ID_FIELD_NUMBER: _ClassVar[int]
    BET_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    idempotency_key: str
    reservation_id: str
    bet_id: str
    reason: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        idempotency_key: str | None = ...,
        reservation_id: str | None = ...,
        bet_id: str | None = ...,
        reason: str | None = ...,
    ) -> None: ...

class ReleaseReservationResponse(_message.Message):
    __slots__ = ("reservation", "wallet")
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    WALLET_FIELD_NUMBER: _ClassVar[int]
    reservation: ReservationSnapshot
    wallet: WalletSnapshot
    def __init__(
        self,
        reservation: ReservationSnapshot | _Mapping | None = ...,
        wallet: WalletSnapshot | _Mapping | None = ...,
    ) -> None: ...

class CreditRewardRequest(_message.Message):
    __slots__ = (
        "amount",
        "context",
        "idempotency_key",
        "identity_user_id",
        "reward_reference_id",
    )
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    idempotency_key: str
    identity_user_id: str
    reward_reference_id: str
    amount: Money
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        idempotency_key: str | None = ...,
        identity_user_id: str | None = ...,
        reward_reference_id: str | None = ...,
        amount: Money | _Mapping | None = ...,
    ) -> None: ...

class CreditRewardResponse(_message.Message):
    __slots__ = ("ledger_entry", "wallet")
    WALLET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ENTRY_FIELD_NUMBER: _ClassVar[int]
    wallet: WalletSnapshot
    ledger_entry: LedgerEntrySnapshot
    def __init__(
        self,
        wallet: WalletSnapshot | _Mapping | None = ...,
        ledger_entry: LedgerEntrySnapshot | _Mapping | None = ...,
    ) -> None: ...

class AdjustBalanceRequest(_message.Message):
    __slots__ = (
        "amount",
        "context",
        "direction",
        "idempotency_key",
        "identity_user_id",
        "reason",
    )
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    idempotency_key: str
    identity_user_id: str
    direction: LedgerDirection
    amount: Money
    reason: str
    def __init__(
        self,
        context: RequestContext | _Mapping | None = ...,
        idempotency_key: str | None = ...,
        identity_user_id: str | None = ...,
        direction: LedgerDirection | str | None = ...,
        amount: Money | _Mapping | None = ...,
        reason: str | None = ...,
    ) -> None: ...

class AdjustBalanceResponse(_message.Message):
    __slots__ = ("ledger_entry", "wallet")
    WALLET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ENTRY_FIELD_NUMBER: _ClassVar[int]
    wallet: WalletSnapshot
    ledger_entry: LedgerEntrySnapshot
    def __init__(
        self,
        wallet: WalletSnapshot | _Mapping | None = ...,
        ledger_entry: LedgerEntrySnapshot | _Mapping | None = ...,
    ) -> None: ...
