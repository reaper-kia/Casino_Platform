from argon2 import PasswordHasher as Argon2LibHasher
from argon2.exceptions import InvalidHashError, VerificationError

from identity_service.applications.ports.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self._hasher = Argon2LibHasher()

    def hash(self, raw_password: str) -> str:
        return self._hasher.hash(raw_password)

    def verify(self, raw_password: str, password_hash: str) -> bool:
        try:
            return self._hasher.verify(password_hash, raw_password)
        except (VerificationError, InvalidHashError):
            return False
