# domain/exceptions.py


class DomainError(Exception):
    """Базовое исключение для всех доменных ошибок."""


# --- Ошибки, связанные с поиском сущностей ---
class PlayerNotFoundError(DomainError):
    """Игрок не найден по identity_user_id."""


class RoomNotFoundError(DomainError):
    """Комната не найдена по ID."""


class ParticipantNotFoundError(DomainError):
    """Участник не найден."""


# --- Ошибки идемпотентности ---
class IdempotencyConflictError(DomainError):
    """Тот же ключ идемпотентности, но разные данные."""


# --- Ошибки валидации ---
class ValidationError(DomainError):
    """Общая ошибка валидации входных данных."""


class InvalidRoomVisibilityError(ValidationError):
    """Некорректное значение visibility (должно быть 'public' или 'private')."""


class InvalidMaxPlayersError(ValidationError):
    """Некорректное значение max_players (должно быть >= 2)."""


class InvalidGameTypeError(ValidationError):
    """Некорректный тип игры."""


# --- Ошибки бизнес-правил (для будущих сценариев) ---
class RoomAlreadyClosedError(DomainError):
    """Попытка выполнить операцию над закрытой комнатой."""


class RoomFullError(DomainError):
    """Комната заполнена (достигнута максимальная вместимость)."""


class PlayerAlreadyInRoomError(DomainError):
    """Игрок уже находится в этой комнате."""


class PlayerNotInRoomError(DomainError):
    """Игрок не является участником комнаты."""


# --- Инфраструктурные ошибки (для репозиториев, если понадобятся) ---
class RepositoryError(Exception):
    """Базовое исключение для ошибок репозитория (не домен)."""


class DuplicateKeyError(RepositoryError):
    """Нарушение уникальности (например, дублирование ключа идемпотентности)."""


class InvalidRoomNameError(Exception):
    pass


class InvalidRoomCapacityError(Exception):
    pass
