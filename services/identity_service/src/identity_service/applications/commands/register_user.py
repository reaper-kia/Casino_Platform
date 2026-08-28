from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    nickname: str
    email: str
    password: str
