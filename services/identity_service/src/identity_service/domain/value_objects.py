from dataclasses import dataclass

from identity_service.domain.exceptions import (
    InvalidEmailError,
    InvalidNicknameError,
    WeakPasswordError,
)


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise InvalidEmailError("Email cannt't be empy")

        if not "@" in self.value:
            raise InvalidEmailError("Invalid email format")


@dataclass(frozen=True)
class Nickname:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise InvalidNicknameError("Nickname cann't be empty")

        if len(self.value) > 255:
            raise InvalidNicknameError("Nickname is too long")


@dataclass(frozen=True)
class RawPassword:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 8:
            raise WeakPasswordError("Password must contain at least 8 characters")

        if len(self.value) > 128:
            raise WeakPasswordError("Password is too long")
