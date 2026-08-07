import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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
    __slots__ = ("request_id", "actor_identity_user_id", "permissions")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    actor_identity_user_id: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, request_id: _Optional[str] = ..., actor_identity_user_id: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class Money(_message.Message):
    __slots__ = ("amount_minor", "currency")
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    amount_minor: int
    currency: str
    def __init__(self, amount_minor: _Optional[int] = ..., currency: _Optional[str] = ...) -> None: ...

class WalletSnapshot(_message.Message):
    __slots__ = ("wallet_account_id", "identity_user_id", "accounting_balance", "reserved_amount", "available_balance", "status", "version", "created_at", "updated_at")
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
    def __init__(self, wallet_account_id: _Optional[str] = ..., identity_user_id: _Optional[str] = ..., accounting_balance: _Optional[_Union[Money, _Mapping]] = ..., reserved_amount: _Optional[_Union[Money, _Mapping]] = ..., available_balance: _Optional[_Union[Money, _Mapping]] = ..., status: _Optional[_Union[WalletStatus, str]] = ..., version: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReservationSnapshot(_message.Message):
    __slots__ = ("reservation_id", "wallet_account_id", "bet_id", "amount", "status", "expires_at", "created_at", "completed_at")
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
    def __init__(self, reservation_id: _Optional[str] = ..., wallet_account_id: _Optional[str] = ..., bet_id: _Optional[str] = ..., amount: _Optional[_Union[Money, _Mapping]] = ..., status: _Optional[_Union[ReservationStatus, str]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LedgerEntrySnapshot(_message.Message):
    __slots__ = ("ledger_entry_id", "wallet_account_id", "operation_id", "entry_type", "direction", "amount", "balance_after", "reference_id", "created_at")
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
    def __init__(self, ledger_entry_id: _Optional[str] = ..., wallet_account_id: _Optional[str] = ..., operation_id: _Optional[str] = ..., entry_type: _Optional[_Union[LedgerEntryType, str]] = ..., direction: _Optional[_Union[LedgerDirection, str]] = ..., amount: _Optional[_Union[Money, _Mapping]] = ..., balance_after: _Optional[_Union[Money, _Mapping]] = ..., reference_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetWalletRequest(_message.Message):
    __slots__ = ("context", "identity_user_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    context: RequestContext
    identity_user_id: str
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., identity_user_id: _Optional[str] = ...) -> None: ...

class GetWalletResponse(_message.Message):
    __slots__ = ("wallet",)
    WALLET_FIELD_NUMBER: _ClassVar[int]
    wallet: WalletSnapshot
    def __init__(self, wallet: _Optional[_Union[WalletSnapshot, _Mapping]] = ...) -> None: ...

class ListLedgerEntriesRequest(_message.Message):
    __slots__ = ("context", "identity_user_id", "entry_type", "direction", "limit", "cursor")
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
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., identity_user_id: _Optional[str] = ..., entry_type: _Optional[_Union[LedgerEntryType, str]] = ..., direction: _Optional[_Union[LedgerDirection, str]] = ..., limit: _Optional[int] = ..., cursor: _Optional[str] = ...) -> None: ...

class ListLedgerEntriesResponse(_message.Message):
    __slots__ = ("entries", "next_cursor")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[LedgerEntrySnapshot]
    next_cursor: str
    def __init__(self, entries: _Optional[_Iterable[_Union[LedgerEntrySnapshot, _Mapping]]] = ..., next_cursor: _Optional[str] = ...) -> None: ...

class ReserveFundsRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "identity_user_id", "bet_id", "amount", "expires_at")
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
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., idempotency_key: _Optional[str] = ..., identity_user_id: _Optional[str] = ..., bet_id: _Optional[str] = ..., amount: _Optional[_Union[Money, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReserveFundsResponse(_message.Message):
    __slots__ = ("reservation", "wallet")
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    WALLET_FIELD_NUMBER: _ClassVar[int]
    reservation: ReservationSnapshot
    wallet: WalletSnapshot
    def __init__(self, reservation: _Optional[_Union[ReservationSnapshot, _Mapping]] = ..., wallet: _Optional[_Union[WalletSnapshot, _Mapping]] = ...) -> None: ...

class SettleBetRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "reservation_id", "bet_id", "payout")
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
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., idempotency_key: _Optional[str] = ..., reservation_id: _Optional[str] = ..., bet_id: _Optional[str] = ..., payout: _Optional[_Union[Money, _Mapping]] = ...) -> None: ...

class SettleBetResponse(_message.Message):
    __slots__ = ("reservation", "wallet", "ledger_entries")
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    WALLET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    reservation: ReservationSnapshot
    wallet: WalletSnapshot
    ledger_entries: _containers.RepeatedCompositeFieldContainer[LedgerEntrySnapshot]
    def __init__(self, reservation: _Optional[_Union[ReservationSnapshot, _Mapping]] = ..., wallet: _Optional[_Union[WalletSnapshot, _Mapping]] = ..., ledger_entries: _Optional[_Iterable[_Union[LedgerEntrySnapshot, _Mapping]]] = ...) -> None: ...

class ReleaseReservationRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "reservation_id", "bet_id", "reason")
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
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., idempotency_key: _Optional[str] = ..., reservation_id: _Optional[str] = ..., bet_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class ReleaseReservationResponse(_message.Message):
    __slots__ = ("reservation", "wallet")
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    WALLET_FIELD_NUMBER: _ClassVar[int]
    reservation: ReservationSnapshot
    wallet: WalletSnapshot
    def __init__(self, reservation: _Optional[_Union[ReservationSnapshot, _Mapping]] = ..., wallet: _Optional[_Union[WalletSnapshot, _Mapping]] = ...) -> None: ...

class CreditRewardRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "identity_user_id", "reward_reference_id", "amount")
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
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., idempotency_key: _Optional[str] = ..., identity_user_id: _Optional[str] = ..., reward_reference_id: _Optional[str] = ..., amount: _Optional[_Union[Money, _Mapping]] = ...) -> None: ...

class CreditRewardResponse(_message.Message):
    __slots__ = ("wallet", "ledger_entry")
    WALLET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ENTRY_FIELD_NUMBER: _ClassVar[int]
    wallet: WalletSnapshot
    ledger_entry: LedgerEntrySnapshot
    def __init__(self, wallet: _Optional[_Union[WalletSnapshot, _Mapping]] = ..., ledger_entry: _Optional[_Union[LedgerEntrySnapshot, _Mapping]] = ...) -> None: ...

class AdjustBalanceRequest(_message.Message):
    __slots__ = ("context", "idempotency_key", "identity_user_id", "direction", "amount", "reason")
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
    def __init__(self, context: _Optional[_Union[RequestContext, _Mapping]] = ..., idempotency_key: _Optional[str] = ..., identity_user_id: _Optional[str] = ..., direction: _Optional[_Union[LedgerDirection, str]] = ..., amount: _Optional[_Union[Money, _Mapping]] = ..., reason: _Optional[str] = ...) -> None: ...

class AdjustBalanceResponse(_message.Message):
    __slots__ = ("wallet", "ledger_entry")
    WALLET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ENTRY_FIELD_NUMBER: _ClassVar[int]
    wallet: WalletSnapshot
    ledger_entry: LedgerEntrySnapshot
    def __init__(self, wallet: _Optional[_Union[WalletSnapshot, _Mapping]] = ..., ledger_entry: _Optional[_Union[LedgerEntrySnapshot, _Mapping]] = ...) -> None: ...
