# domain/exceptions.py

class DomainError(Exception):
    """Базовое исключение для всех доменных ошибок."""
    pass


# --- Ошибки, связанные с поиском сущностей ---
class PlayerNotFoundError(DomainError):
    """Игрок не найден по identity_user_id."""
    pass


class RoomNotFoundError(DomainError):
    """Комната не найдена по ID."""
    pass


class ParticipantNotFoundError(DomainError):
    """Участник не найден."""
    pass


# --- Ошибки идемпотентности ---
class IdempotencyConflictError(DomainError):
    """Тот же ключ идемпотентности, но разные данные."""
    pass


# --- Ошибки валидации ---
class ValidationError(DomainError):
    """Общая ошибка валидации входных данных."""
    pass


class InvalidRoomVisibilityError(ValidationError):
    """Некорректное значение visibility (должно быть 'public' или 'private')."""
    pass


class InvalidMaxPlayersError(ValidationError):
    """Некорректное значение max_players (должно быть >= 2)."""
    pass


class InvalidGameTypeError(ValidationError):
    """Некорректный тип игры."""
    pass


# --- Ошибки бизнес-правил (для будущих сценариев) ---
class RoomAlreadyClosedError(DomainError):
    """Попытка выполнить операцию над закрытой комнатой."""
    pass


class RoomFullError(DomainError):
    """Комната заполнена (достигнута максимальная вместимость)."""
    pass


class PlayerAlreadyInRoomError(DomainError):
    """Игрок уже находится в этой комнате."""
    pass


class PlayerNotInRoomError(DomainError):
    """Игрок не является участником комнаты."""
    pass


# --- Инфраструктурные ошибки (для репозиториев, если понадобятся) ---
class RepositoryError(Exception):
    """Базовое исключение для ошибок репозитория (не домен)."""
    pass


class DuplicateKeyError(RepositoryError):
    """Нарушение уникальности (например, дублирование ключа идемпотентности)."""
    pass