# Gateway API v1

Статус: контракт для начала параллельной разработки.

Документ описывает публичное взаимодействие:

- Frontend → Gateway по HTTP;
- Frontend ↔ Gateway по WebSocket.

Frontend не импортирует `.proto` и не обращается к внутренним сервисам напрямую.

---

## 1. Общие правила

### 1.1 Адреса

- HTTP base path: `/api/v1`
- WebSocket path: `/ws/v1`
- OpenAPI в локальном окружении: `/docs`
- Health check: `/health/live`

### 1.2 Формат данных

- HTTP и WebSocket используют JSON;
- названия JSON-полей записываются в `snake_case`;
- UUID передаётся строкой;
- время передаётся в формате RFC 3339 UTC;
- отсутствующее значение передаётся как `null`;
- деньги никогда не передаются через `float`;
- неизвестные значения enum frontend не должен считать допустимыми.

Пример времени:

```json
"2026-08-08T12:40:00.250Z"
```

Пример UUID:

```json
"0d92d7df-1e24-4a17-97b7-99417480e1c5"
```

### 1.3 Money

```json
{
  "amount_minor": 1050,
  "currency": "USD"
}
```

`1050 USD` означает `$10.50`.

На первом этапе поддерживается только валюта `USD`.

Frontend использует JavaScript `number`, поэтому backend не должен возвращать `amount_minor` выше `Number.MAX_SAFE_INTEGER`.

### 1.4 Авторизация

Защищённые HTTP-запросы передают access token:

```http
Authorization: Bearer <access-token>
```

Refresh token:

- передаётся только через `HttpOnly` cookie;
- не сохраняется frontend-кодом;
- не передаётся в URL;
- не возвращается в JSON;
- заменяется при успешном refresh.

### 1.5 Request ID

Frontend может передать:

```http
X-Request-ID: <uuid>
```

Если заголовок отсутствует, Gateway создаёт UUID самостоятельно.

Gateway возвращает итоговый идентификатор:

```http
X-Request-ID: <uuid>
```

`request_id` используется для:

- поиска связанных логов;
- tracing;
- сопоставления WebSocket-команды с ответом.

`request_id` не обеспечивает идемпотентность.

### 1.6 Idempotency Key

Для указанных ниже изменяющих состояние команд frontend передаёт:

```http
Idempotency-Key: <uuid>
```

В WebSocket-командах ключ находится в поле `idempotency_key`.

Ключ обязателен для:

- создания комнаты;
- входа в комнату;
- выхода из комнаты;
- создания ставки;
- отмены ставки;
- игровых действий.

Повтор запроса с тем же ключом и тем же payload должен вернуть прежний результат без повторного выполнения операции.

Повтор ключа с другим payload возвращает:

```http
409 Conflict
```

```json
{
  "error": {
    "code": "IDEMPOTENCY_KEY_REUSED",
    "message": "Idempotency key was already used with another request",
    "request_id": "uuid",
    "details": []
  }
}
```

После timeout frontend повторяет команду только с прежним `idempotency_key`.

---

## 2. Ошибки

Единый формат ошибки:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "request_id": "0d92d7df-1e24-4a17-97b7-99417480e1c5",
    "details": [
      {
        "field": "email",
        "reason": "invalid_format"
      }
    ]
  }
}
```

Правила:

- `code` предназначен для логики frontend;
- `message` предназначен для разработки и не обязательно показывается пользователю;
- `details` всегда является массивом;
- Gateway не возвращает stack trace;
- Gateway не возвращает SQL, внутренние адреса или текст необработанного исключения;
- frontend не принимает решения на основании `message`.

Основные публичные коды:

| HTTP | `code` | Значение |
|---:|---|---|
| 400 | `BAD_REQUEST` | Некорректный запрос |
| 401 | `UNAUTHENTICATED` | Нет действующей авторизации |
| 403 | `PERMISSION_DENIED` | Недостаточно прав |
| 404 | `USER_NOT_FOUND` | Пользователь не найден |
| 404 | `WALLET_NOT_FOUND` | Wallet не найден |
| 404 | `ROOM_NOT_FOUND` | Комната не найдена |
| 404 | `ROUND_NOT_FOUND` | Раунд не найден |
| 404 | `BET_NOT_FOUND` | Ставка не найдена |
| 409 | `ALREADY_EXISTS` | Ресурс уже существует |
| 409 | `IDEMPOTENCY_KEY_REUSED` | Ключ повторён с другим payload |
| 409 | `STALE_REVISION` | Состояние уже изменилось |
| 409 | `INVALID_STATE_TRANSITION` | Операция невозможна в текущем состоянии |
| 422 | `VALIDATION_ERROR` | Ошибка валидации |
| 429 | `RATE_LIMITED` | Превышено ограничение запросов |
| 503 | `WALLET_PROVISIONING` | Wallet ещё создаётся |
| 503 | `SERVICE_UNAVAILABLE` | Внутренний сервис временно недоступен |
| 504 | `UPSTREAM_TIMEOUT` | Внутренний сервис не ответил вовремя |

---

## 3. Pagination

Списочные ручки используют cursor pagination.

Request:

```text
?limit=20&cursor=<opaque-value>
```

Response:

```json
{
  "items": [],
  "next_cursor": null
}
```

Правила:

- `limit`: от `1` до `100`;
- значение по умолчанию: `20`;
- `cursor` является непрозрачной строкой;
- frontend не разбирает содержимое cursor;
- `next_cursor: null` означает, что следующей страницы нет.

---

## 4. Auth

### 4.1 Регистрация

```http
POST /api/v1/auth/register
Content-Type: application/json
```

Авторизация не требуется.

Request:

```json
{
  "email": "player@example.com",
  "nickname": "player_one",
  "password": "plain password received over HTTPS"
}
```

Response:

```http
201 Created
Set-Cookie: refresh_token=<opaque-value>; HttpOnly; SameSite=Lax
```

```json
{
  "user": {
    "user_id": "uuid",
    "email": "player@example.com",
    "nickname": "player_one",
    "role": "player",
    "status": "active",
    "created_at": "2026-08-08T12:30:00Z",
    "updated_at": "2026-08-08T12:30:00Z"
  },
  "access_token": "jwt",
  "access_token_expires_at": "2026-08-08T12:45:00Z"
}
```

Особенности:

- Wallet создаётся асинхронно;
- CasinoPlayer создаётся асинхронно;
- Wallet и CasinoPlayer не входят в ответ регистрации;
- email нормализуется backend;
- пароль никогда не записывается в логи.

Внутренний RPC:

```text
IdentityService.Register
```

Возможные ошибки:

- `409 ALREADY_EXISTS`;
- `422 VALIDATION_ERROR`;
- `503 SERVICE_UNAVAILABLE`;
- `504 UPSTREAM_TIMEOUT`.

### 4.2 Вход

```http
POST /api/v1/auth/login
Content-Type: application/json
```

Request:

```json
{
  "email": "player@example.com",
  "password": "plain password received over HTTPS"
}
```

Response:

```http
200 OK
Set-Cookie: refresh_token=<opaque-value>; HttpOnly; SameSite=Lax
```

```json
{
  "user": {
    "user_id": "uuid",
    "email": "player@example.com",
    "nickname": "player_one",
    "role": "player",
    "status": "active",
    "created_at": "2026-08-08T12:30:00Z",
    "updated_at": "2026-08-08T12:30:00Z"
  },
  "access_token": "jwt",
  "access_token_expires_at": "2026-08-08T12:45:00Z"
}
```

Внутренний RPC:

```text
IdentityService.Login
```

### 4.3 Обновление токенов

```http
POST /api/v1/auth/refresh
Cookie: refresh_token=<opaque-value>
```

Тело отсутствует.

Response:

```http
200 OK
Set-Cookie: refresh_token=<new-opaque-value>; HttpOnly; SameSite=Lax
```

```json
{
  "access_token": "jwt",
  "access_token_expires_at": "2026-08-08T13:00:00Z"
}
```

Старый refresh token после успешной ротации больше не используется.

Внутренний RPC:

```text
IdentityService.RefreshToken
```

### 4.4 Выход

```http
POST /api/v1/auth/logout
Authorization: Bearer <access-token>
Cookie: refresh_token=<opaque-value>
Content-Type: application/json
```

Request:

```json
{
  "all_sessions": false
}
```

Если `all_sessions=true`, Identity отзывает все refresh-сессии пользователя.

Response:

```http
204 No Content
```

Операция является естественно идемпотентной: повторный logout также возвращает `204`.

Gateway удаляет refresh cookie.

Внутренний RPC:

```text
IdentityService.Logout
```

---

## 5. User

### 5.1 Текущий пользователь

```http
GET /api/v1/users/me
Authorization: Bearer <access-token>
```

Response:

```http
200 OK
```

```json
{
  "user_id": "uuid",
  "email": "player@example.com",
  "nickname": "player_one",
  "role": "player",
  "status": "active",
  "created_at": "2026-08-08T12:30:00Z",
  "updated_at": "2026-08-08T12:30:00Z"
}
```

Значения `role`:

- `player`;
- `admin`.

Значения `status`:

- `active`;
- `blocked`;
- `deleted`.

Внутренний RPC:

```text
IdentityService.GetMe
```

---

## 6. Wallet

### 6.1 Текущий Wallet

```http
GET /api/v1/wallet/me
Authorization: Bearer <access-token>
```

Response:

```http
200 OK
```

```json
{
  "wallet_account_id": "uuid",
  "identity_user_id": "uuid",
  "accounting_balance": {
    "amount_minor": 100000,
    "currency": "USD"
  },
  "reserved_amount": {
    "amount_minor": 5000,
    "currency": "USD"
  },
  "available_balance": {
    "amount_minor": 95000,
    "currency": "USD"
  },
  "status": "active",
  "version": 7,
  "created_at": "2026-08-08T12:30:00Z",
  "updated_at": "2026-08-08T12:40:00Z"
}
```

Значения `status`:

- `active`;
- `frozen`;
- `closed`.

Правило баланса:

```text
available_balance = accounting_balance - reserved_amount
```

Пока Wallet создаётся после регистрации, Gateway возвращает:

```http
503 Service Unavailable
Retry-After: 1
```

```json
{
  "error": {
    "code": "WALLET_PROVISIONING",
    "message": "Wallet is being provisioned",
    "request_id": "uuid",
    "details": []
  }
}
```

Внутренний RPC:

```text
WalletService.GetWallet
```

### 6.2 Ledger

```http
GET /api/v1/wallet/me/ledger
Authorization: Bearer <access-token>
```

Query parameters:

| Параметр | Обязательный | Значения |
|---|---|---|
| `entry_type` | Нет | `initial_grant`, `bet_settlement`, `bonus`, `admin_adjustment` |
| `direction` | Нет | `credit`, `debit` |
| `limit` | Нет | `1..100` |
| `cursor` | Нет | opaque cursor |

Response:

```json
{
  "items": [
    {
      "ledger_entry_id": "uuid",
      "operation_id": "uuid",
      "entry_type": "bet_settlement",
      "direction": "debit",
      "amount": {
        "amount_minor": 5000,
        "currency": "USD"
      },
      "balance_after": {
        "amount_minor": 95000,
        "currency": "USD"
      },
      "reference_id": "bet-uuid",
      "created_at": "2026-08-08T12:40:00Z"
    }
  ],
  "next_cursor": null
}
```

Внутренний RPC:

```text
WalletService.ListLedgerEntries
```

---

## 7. Casino rooms

### 7.1 Список комнат

```http
GET /api/v1/casino/rooms
Authorization: Bearer <access-token>
```

Query parameters:

| Параметр | Обязательный | Значения |
|---|---|---|
| `game_type` | Нет | `dice_duel`, `crash`, `roulette` |
| `visibility` | Нет | `public`, `private` |
| `status` | Нет | `open`, `closed`, `archived` |
| `limit` | Нет | `1..100` |
| `cursor` | Нет | opaque cursor |

Response:

```json
{
  "items": [
    {
      "room_id": "uuid",
      "name": "Crash Main",
      "game_type": "crash",
      "visibility": "public",
      "status": "open",
      "capacity": 100,
      "participants_count": 12,
      "revision": 42,
      "owner_player_id": null,
      "is_system": true,
      "created_at": "2026-08-08T12:00:00Z",
      "updated_at": "2026-08-08T12:40:00Z",
      "closed_at": null
    }
  ],
  "next_cursor": null
}
```

Внутренний RPC:

```text
CasinoRoomService.ListRooms
```

### 7.2 Создание комнаты

```http
POST /api/v1/casino/rooms
Authorization: Bearer <access-token>
Idempotency-Key: <uuid>
Content-Type: application/json
```

Request:

```json
{
  "name": "Private Dice",
  "game_type": "dice_duel",
  "visibility": "private",
  "capacity": 2
}
```

Response:

```http
201 Created
```

```json
{
  "snapshot": {
    "room": {
      "room_id": "uuid",
      "name": "Private Dice",
      "game_type": "dice_duel",
      "visibility": "private",
      "status": "open",
      "capacity": 2,
      "participants_count": 0,
      "revision": 1,
      "owner_player_id": "uuid",
      "is_system": false,
      "created_at": "2026-08-08T12:40:00Z",
      "updated_at": "2026-08-08T12:40:00Z",
      "closed_at": null
    },
    "participants": [],
    "server_time": "2026-08-08T12:40:00Z"
  },
  "invite_token": "returned-only-on-creation"
}
```

Для публичной комнаты:

```json
"invite_token": null
```

Для приватной комнаты исходный `invite_token` возвращается только при создании. Casino хранит только его безопасное представление.

Внутренний RPC:

```text
CasinoRoomService.CreateRoom
```

### 7.3 Snapshot комнаты

```http
GET /api/v1/casino/rooms/{room_id}
Authorization: Bearer <access-token>
```

Response:

```json
{
  "room": {
    "room_id": "uuid",
    "name": "Crash Main",
    "game_type": "crash",
    "visibility": "public",
    "status": "open",
    "capacity": 100,
    "participants_count": 2,
    "revision": 42,
    "owner_player_id": null,
    "is_system": true,
    "created_at": "2026-08-08T12:00:00Z",
    "updated_at": "2026-08-08T12:40:00Z",
    "closed_at": null
  },
  "participants": [
    {
      "participant_id": "uuid",
      "player": {
        "player_id": "uuid",
        "identity_user_id": "uuid",
        "nickname": "player_one",
        "avatar_url": null,
        "status": "active",
        "updated_at": "2026-08-08T12:40:00Z"
      },
      "seat": 1,
      "membership_status": "active",
      "connection_status": "connected",
      "joined_at": "2026-08-08T12:40:00Z",
      "disconnected_at": null,
      "reconnect_deadline": null,
      "left_at": null
    }
  ],
  "server_time": "2026-08-08T12:40:00Z"
}
```

Значения `membership_status`:

- `active`;
- `left`.

Значения `connection_status`:

- `connected`;
- `disconnected`.

Внутренний RPC:

```text
CasinoRoomService.GetRoomSnapshot
```

---

## 8. Casino rounds

### 8.1 RoundSummary

```json
{
  "round_id": "uuid",
  "room_id": "uuid",
  "game_type": "crash",
  "round_number": 18,
  "status": "running",
  "revision": 57,
  "configuration_version": "crash-v1",
  "created_at": "2026-08-08T12:39:00Z",
  "betting_started_at": "2026-08-08T12:39:30Z",
  "started_at": "2026-08-08T12:40:00Z",
  "completed_at": null
}
```

Значения `status`:

- `scheduled`;
- `betting`;
- `locked`;
- `running`;
- `settlement_pending`;
- `completed`;
- `cancelled`.

### 8.2 RoundSnapshot

До завершения раунда `result` равен `null`.

```json
{
  "round": {
    "round_id": "uuid",
    "room_id": "uuid",
    "game_type": "crash",
    "round_number": 18,
    "status": "running",
    "revision": 57,
    "configuration_version": "crash-v1",
    "created_at": "2026-08-08T12:39:00Z",
    "betting_started_at": "2026-08-08T12:39:30Z",
    "started_at": "2026-08-08T12:40:00Z",
    "completed_at": null
  },
  "fairness": {
    "server_seed_hash": "hex-string",
    "server_seed": null,
    "client_seed": "public-client-seed",
    "nonce": 18,
    "algorithm_version": "provably-fair-v1"
  },
  "result": null
}
```

После завершения Crash:

```json
{
  "type": "crash",
  "crash_multiplier_millis": 2384
}
```

`2384` означает коэффициент `2.384x`.

После завершения Roulette:

```json
{
  "type": "roulette",
  "winning_pocket": "17",
  "color": "black"
}
```

Цвет:

- `red`;
- `black`;
- `green`.

После завершения Dice Duel:

```json
{
  "type": "dice_duel",
  "player_rolls": [
    {
      "player_id": "uuid",
      "values": [4, 6],
      "total": 10
    },
    {
      "player_id": "uuid",
      "values": [2, 5],
      "total": 7
    }
  ],
  "winner_player_id": "uuid"
}
```

При ничьей:

```json
"winner_player_id": null
```

После завершения раунда `fairness.server_seed` содержит раскрытый seed.

### 8.3 Текущий раунд комнаты

```http
GET /api/v1/casino/rooms/{room_id}/rounds/current
Authorization: Bearer <access-token>
```

Response:

```http
200 OK
```

```json
{
  "round": {
    "round_id": "uuid",
    "room_id": "uuid",
    "game_type": "crash",
    "round_number": 18,
    "status": "betting",
    "revision": 12,
    "configuration_version": "crash-v1",
    "created_at": "2026-08-08T12:39:00Z",
    "betting_started_at": "2026-08-08T12:39:30Z",
    "started_at": null,
    "completed_at": null
  },
  "fairness": {
    "server_seed_hash": "hex-string",
    "server_seed": null,
    "client_seed": "public-client-seed",
    "nonce": 18,
    "algorithm_version": "provably-fair-v1"
  },
  "result": null
}
```

Если текущего раунда нет:

```http
404 Not Found
```

```json
{
  "error": {
    "code": "ROUND_NOT_FOUND",
    "message": "Current round was not found",
    "request_id": "uuid",
    "details": []
  }
}
```

Внутренний RPC:

```text
CasinoRoundService.GetCurrentRound
```

### 8.4 История раундов

```http
GET /api/v1/casino/rooms/{room_id}/rounds
Authorization: Bearer <access-token>
```

Query parameters:

| Параметр | Обязательный | Значения |
|---|---|---|
| `status` | Нет | Любой Round status |
| `limit` | Нет | `1..100` |
| `cursor` | Нет | opaque cursor |

Response:

```json
{
  "items": [
    {
      "round_id": "uuid",
      "room_id": "uuid",
      "game_type": "roulette",
      "round_number": 17,
      "status": "completed",
      "revision": 81,
      "configuration_version": "roulette-v1",
      "created_at": "2026-08-08T12:35:00Z",
      "betting_started_at": "2026-08-08T12:35:10Z",
      "started_at": "2026-08-08T12:35:30Z",
      "completed_at": "2026-08-08T12:35:35Z"
    }
  ],
  "next_cursor": null
}
```

Внутренний RPC:

```text
CasinoRoundService.ListRounds
```

---

## 9. Casino bets

### 9.1 BetSnapshot

```json
{
  "bet_id": "uuid",
  "round_id": "uuid",
  "player_id": "uuid",
  "amount": {
    "amount_minor": 5000,
    "currency": "USD"
  },
  "selection": {
    "type": "crash",
    "auto_cash_out_multiplier_millis": 2000
  },
  "status": "accepted",
  "payout": null,
  "wallet_reservation_id": "uuid",
  "created_at": "2026-08-08T12:39:35Z",
  "accepted_at": "2026-08-08T12:39:36Z",
  "settled_at": null
}
```

Значения `status`:

- `pending_reservation`;
- `accepted`;
- `rejected`;
- `settlement_pending`;
- `settled`;
- `cancelled`.

До settlement:

```json
"payout": null
```

После settlement:

```json
"payout": {
  "amount_minor": 10000,
  "currency": "USD"
}
```

`payout` означает полную сумму возврата игроку, включая возвращаемую ставку.

Для проигравшей ставки:

```json
"payout": {
  "amount_minor": 0,
  "currency": "USD"
}
```

### 9.2 История ставок текущего пользователя

```http
GET /api/v1/casino/bets/me
Authorization: Bearer <access-token>
```

Query parameters:

| Параметр | Обязательный | Значения |
|---|---|---|
| `round_id` | Нет | UUID раунда |
| `status` | Нет | Любой Bet status |
| `limit` | Нет | `1..100` |
| `cursor` | Нет | opaque cursor |

Response:

```json
{
  "items": [
    {
      "bet_id": "uuid",
      "round_id": "uuid",
      "player_id": "uuid",
      "amount": {
        "amount_minor": 5000,
        "currency": "USD"
      },
      "selection": {
        "type": "crash",
        "auto_cash_out_multiplier_millis": 2000
      },
      "status": "settled",
      "payout": {
        "amount_minor": 10000,
        "currency": "USD"
      },
      "wallet_reservation_id": "uuid",
      "created_at": "2026-08-08T12:39:35Z",
      "accepted_at": "2026-08-08T12:39:36Z",
      "settled_at": "2026-08-08T12:40:10Z"
    }
  ],
  "next_cursor": null
}
```

Внутренний RPC:

```text
CasinoBetService.ListMyBets
```

---

## 10. Realtime ticket

### 10.1 Получение ticket

```http
POST /api/v1/realtime/ticket
Authorization: Bearer <access-token>
```

Тело отсутствует.

Response:

```http
201 Created
```

```json
{
  "ticket": "single-use-opaque-value",
  "expires_at": "2026-08-08T12:40:30Z"
}
```

Ticket:

- является одноразовым;
- живёт не более 30 секунд;
- хранится в Redis;
- связан с конкретным пользователем;
- удаляется после успешного открытия WebSocket;
- не записывается в логи.

Access token не передаётся в URL WebSocket.

---

## 11. WebSocket

### 11.1 Подключение

```text
wss://host/ws/v1?ticket=<single-use-ticket>
```

В локальном окружении:

```text
ws://localhost:8000/ws/v1?ticket=<single-use-ticket>
```

После подключения Gateway отправляет:

```json
{
  "type": "connection.ready",
  "event_id": "uuid",
  "request_id": null,
  "room_id": null,
  "revision": null,
  "occurred_at": "2026-08-08T12:40:00Z",
  "payload": {
    "identity_user_id": "uuid",
    "heartbeat_interval_seconds": 20
  }
}
```

Frontend использует стандартные WebSocket ping/pong механизмы библиотеки или браузера. При потере соединения выполняется reconnect flow.

### 11.2 Формат команды клиента

```json
{
  "type": "bet.place",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {}
}
```

Правила:

- `type` определяет команду;
- `request_id` обязателен;
- `idempotency_key` обязателен для изменяющих состояние команд;
- `payload` всегда является объектом;
- одна команда содержит ровно одно действие;
- повтор команды использует прежний `idempotency_key`;
- новый пользовательский запрос использует новый ключ.

### 11.3 `room.join`

```json
{
  "type": "room.join",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "room_id": "uuid",
    "invite_token": null
  }
}
```

Для приватной комнаты:

```json
"invite_token": "opaque-invite-token"
```

Внутренний RPC:

```text
CasinoRoomService.JoinRoom
```

Успешный ответ: `room.snapshot`.

### 11.4 `room.leave`

```json
{
  "type": "room.leave",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "room_id": "uuid"
  }
}
```

Внутренний RPC:

```text
CasinoRoomService.LeaveRoom
```

Успешный ответ: `room.snapshot`.

### 11.5 `room.resume`

```json
{
  "type": "room.resume",
  "request_id": "uuid",
  "idempotency_key": null,
  "payload": {
    "room_id": "uuid",
    "last_revision": 57
  }
}
```

`room.resume` является естественно идемпотентной операцией и всегда возвращает authoritative snapshot.

Внутренний RPC:

```text
CasinoRoomService.ResumeRoomSession
```

Успешный ответ: `room.snapshot`.

### 11.6 `bet.place`: Dice Duel

```json
{
  "type": "bet.place",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "round_id": "uuid",
    "amount": {
      "amount_minor": 5000,
      "currency": "USD"
    },
    "selection": {
      "type": "dice_duel"
    }
  }
}
```

### 11.7 `bet.place`: Crash

```json
{
  "type": "bet.place",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "round_id": "uuid",
    "amount": {
      "amount_minor": 5000,
      "currency": "USD"
    },
    "selection": {
      "type": "crash",
      "auto_cash_out_multiplier_millis": 2000
    }
  }
}
```

`auto_cash_out_multiplier_millis` может быть `null`.

Внутренний RPC:

```text
CasinoBetService.PlaceBet
```

Успешный ответ:

- `bet.accepted`; или
- `bet.rejected`.

### 11.8 `bet.place`: Roulette

```json
{
  "type": "bet.place",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "round_id": "uuid",
    "amount": {
      "amount_minor": 1000,
      "currency": "USD"
    },
    "selection": {
      "type": "roulette",
      "bet_type": "straight",
      "pockets": ["17"]
    }
  }
}
```

Значения `bet_type`:

- `straight`;
- `split`;
- `street`;
- `corner`;
- `line`;
- `dozen`;
- `column`;
- `red`;
- `black`;
- `even`;
- `odd`;
- `low`;
- `high`.

Backend проверяет, что `pockets` соответствует выбранному `bet_type`.

### 11.9 `bet.cancel`

```json
{
  "type": "bet.cancel",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "bet_id": "uuid"
  }
}
```

Внутренний RPC:

```text
CasinoBetService.CancelBet
```

Успешный ответ: `bet.snapshot`.

Отменить можно только ставку текущего пользователя и только пока это разрешает состояние раунда.

### 11.10 `round.action`: Ready

```json
{
  "type": "round.action",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "round_id": "uuid",
    "expected_revision": 12,
    "action": {
      "type": "ready"
    }
  }
}
```

### 11.11 `round.action`: Throw dice

```json
{
  "type": "round.action",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "round_id": "uuid",
    "expected_revision": 13,
    "action": {
      "type": "throw_dice"
    }
  }
}
```

### 11.12 `round.action`: Cash out

```json
{
  "type": "round.action",
  "request_id": "uuid",
  "idempotency_key": "uuid",
  "payload": {
    "round_id": "uuid",
    "expected_revision": 57,
    "action": {
      "type": "cash_out",
      "bet_id": "uuid"
    }
  }
}
```

Внутренний RPC:

```text
CasinoRoundService.SubmitRoundAction
```

Успешный ответ: `round.snapshot`.

---

## 12. Сообщения WebSocket-сервера

### 12.1 Общий envelope

```json
{
  "type": "round.snapshot",
  "event_id": "uuid",
  "request_id": "uuid-or-null",
  "room_id": "uuid-or-null",
  "revision": 58,
  "occurred_at": "2026-08-08T12:40:00.250Z",
  "payload": {}
}
```

Правила:

- `event_id` используется для удаления дубликатов;
- `request_id` заполнен для ответа на конкретную команду;
- у обычного broadcast `request_id=null`;
- `room_id` может быть `null` для глобального события;
- `revision` может быть `null`, если событие не относится к versioned room state;
- frontend игнорирует уже обработанный `event_id`;
- frontend игнорирует room event с revision меньше или равной уже применённой.

### 12.2 Типы сообщений

| `type` | `payload` |
|---|---|
| `connection.ready` | Данные установленного соединения |
| `room.snapshot` | Полный `RoomSnapshot` |
| `room.participant_joined` | `RoomParticipantSnapshot` |
| `room.participant_left` | `RoomParticipantSnapshot` |
| `round.snapshot` | Полный `RoundSnapshot` |
| `round.started` | Полный `RoundSnapshot` |
| `round.completed` | Полный `RoundSnapshot` |
| `bet.snapshot` | Полный `BetSnapshot` |
| `bet.accepted` | Полный `BetSnapshot` |
| `bet.rejected` | Bet и публичный код отказа |
| `bet.settled` | Полный `BetSnapshot` |
| `wallet.balance_updated` | Полный `WalletSnapshot` |
| `error` | Публичная ошибка команды |

### 12.3 `room.snapshot`

```json
{
  "type": "room.snapshot",
  "event_id": "uuid",
  "request_id": "uuid",
  "room_id": "uuid",
  "revision": 43,
  "occurred_at": "2026-08-08T12:40:00Z",
  "payload": {
    "room": {
      "room_id": "uuid",
      "name": "Crash Main",
      "game_type": "crash",
      "visibility": "public",
      "status": "open",
      "capacity": 100,
      "participants_count": 13,
      "revision": 43,
      "owner_player_id": null,
      "is_system": true,
      "created_at": "2026-08-08T12:00:00Z",
      "updated_at": "2026-08-08T12:40:00Z",
      "closed_at": null
    },
    "participants": [],
    "server_time": "2026-08-08T12:40:00Z"
  }
}
```

### 12.4 `round.snapshot`

```json
{
  "type": "round.snapshot",
  "event_id": "uuid",
  "request_id": "uuid",
  "room_id": "uuid",
  "revision": 58,
  "occurred_at": "2026-08-08T12:40:00Z",
  "payload": {
    "round": {
      "round_id": "uuid",
      "room_id": "uuid",
      "game_type": "crash",
      "round_number": 18,
      "status": "running",
      "revision": 58,
      "configuration_version": "crash-v1",
      "created_at": "2026-08-08T12:39:00Z",
      "betting_started_at": "2026-08-08T12:39:30Z",
      "started_at": "2026-08-08T12:40:00Z",
      "completed_at": null
    },
    "fairness": {
      "server_seed_hash": "hex-string",
      "server_seed": null,
      "client_seed": "public-client-seed",
      "nonce": 18,
      "algorithm_version": "provably-fair-v1"
    },
    "result": null
  }
}
```

### 12.5 `bet.accepted`

```json
{
  "type": "bet.accepted",
  "event_id": "uuid",
  "request_id": "uuid",
  "room_id": "uuid",
  "revision": null,
  "occurred_at": "2026-08-08T12:39:36Z",
  "payload": {
    "bet_id": "uuid",
    "round_id": "uuid",
    "player_id": "uuid",
    "amount": {
      "amount_minor": 5000,
      "currency": "USD"
    },
    "selection": {
      "type": "crash",
      "auto_cash_out_multiplier_millis": 2000
    },
    "status": "accepted",
    "payout": null,
    "wallet_reservation_id": "uuid",
    "created_at": "2026-08-08T12:39:35Z",
    "accepted_at": "2026-08-08T12:39:36Z",
    "settled_at": null
  }
}
```

### 12.6 `bet.rejected`

```json
{
  "type": "bet.rejected",
  "event_id": "uuid",
  "request_id": "uuid",
  "room_id": "uuid",
  "revision": null,
  "occurred_at": "2026-08-08T12:39:36Z",
  "payload": {
    "bet": {
      "bet_id": "uuid",
      "round_id": "uuid",
      "player_id": "uuid",
      "amount": {
        "amount_minor": 5000,
        "currency": "USD"
      },
      "selection": {
        "type": "crash",
        "auto_cash_out_multiplier_millis": 2000
      },
      "status": "rejected",
      "payout": null,
      "wallet_reservation_id": null,
      "created_at": "2026-08-08T12:39:35Z",
      "accepted_at": null,
      "settled_at": null
    },
    "code": "INSUFFICIENT_FUNDS"
  }
}
```

Возможные коды:

- `INSUFFICIENT_FUNDS`;
- `WALLET_UNAVAILABLE`;
- `ROUND_NOT_BETTING`;
- `INVALID_SELECTION`;
- `BET_LIMIT_EXCEEDED`.

### 12.7 `wallet.balance_updated`

Payload совпадает с ответом `GET /api/v1/wallet/me`.

```json
{
  "type": "wallet.balance_updated",
  "event_id": "uuid",
  "request_id": null,
  "room_id": null,
  "revision": null,
  "occurred_at": "2026-08-08T12:40:10Z",
  "payload": {
    "wallet_account_id": "uuid",
    "identity_user_id": "uuid",
    "accounting_balance": {
      "amount_minor": 105000,
      "currency": "USD"
    },
    "reserved_amount": {
      "amount_minor": 0,
      "currency": "USD"
    },
    "available_balance": {
      "amount_minor": 105000,
      "currency": "USD"
    },
    "status": "active",
    "version": 8,
    "created_at": "2026-08-08T12:30:00Z",
    "updated_at": "2026-08-08T12:40:10Z"
  }
}
```

### 12.8 WebSocket error

```json
{
  "type": "error",
  "event_id": "uuid",
  "request_id": "uuid",
  "room_id": "uuid",
  "revision": 58,
  "occurred_at": "2026-08-08T12:40:00Z",
  "payload": {
    "code": "STALE_REVISION",
    "message": "Round revision is stale",
    "retryable": true,
    "details": {
      "current_revision": 58
    }
  }
}
```

При `STALE_REVISION` frontend:

1. не повторяет игровую команду автоматически;
2. запрашивает или применяет новый snapshot;
3. показывает пользователю актуальное состояние.

При `SERVICE_UNAVAILABLE` или `UPSTREAM_TIMEOUT` команда повторяется только с прежним `idempotency_key`.

---

## 13. Reconnect

1. Frontend сохраняет последнюю применённую room revision.
2. При разрыве соединения frontend получает новый realtime ticket.
3. Frontend открывает новый WebSocket.
4. Frontend ждёт `connection.ready`.
5. Frontend отправляет `room.resume`.
6. Gateway вызывает `CasinoRoomService.ResumeRoomSession`.
7. Casino возвращает authoritative `RoomSnapshot`.
8. Gateway отправляет `room.snapshot`.
9. Frontend полностью заменяет локальное состояние snapshot-ом.

Frontend не пытается самостоятельно восстановить пропущенные room events.

Snapshot является источником истины после reconnect.

---

## 14. Преобразование gRPC ошибок

| gRPC status | HTTP | Public code |
|---|---:|---|
| `INVALID_ARGUMENT` | 422 | `VALIDATION_ERROR` |
| `UNAUTHENTICATED` | 401 | `UNAUTHENTICATED` |
| `PERMISSION_DENIED` | 403 | `PERMISSION_DENIED` |
| `NOT_FOUND` | 404 | Domain-specific `*_NOT_FOUND` |
| `ALREADY_EXISTS` | 409 | `ALREADY_EXISTS` |
| `FAILED_PRECONDITION` | 409 | Domain-specific state error |
| `ABORTED` | 409 | `STALE_REVISION` или `CONCURRENT_MODIFICATION` |
| `RESOURCE_EXHAUSTED` | 429 | `RATE_LIMITED` |
| `UNAVAILABLE` | 503 | `SERVICE_UNAVAILABLE` |
| `DEADLINE_EXCEEDED` | 504 | `UPSTREAM_TIMEOUT` |
| `INTERNAL` | 502 | `UPSTREAM_ERROR` |

Gateway записывает внутреннюю ошибку в лог вместе с `request_id`, но не раскрывает её frontend.