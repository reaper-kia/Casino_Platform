from dataclasses import dataclass

from identity_service.applications.commands.register_user import RegisterUserCommand
from identity_service.applications.ports.password_hasher import PasswordHasher
from identity_service.applications.ports.unit_of_work import UnitOfWorkFactory
from identity_service.domain.entities import User
from identity_service.domain.exceptions import UserAlreadyRegisterError
from identity_service.domain.value_objects import Email, Nickname, RawPassword


@dataclass
class RegisterUserCommandHandler:
    uow_factory: UnitOfWorkFactory
    password_hasher: PasswordHasher

    async def handle(self, cmd: RegisterUserCommand) -> None:
        email = Email(cmd.email)
        nickname = Nickname(cmd.nickname)
        raw_password = RawPassword(cmd.password)

        async with self.uow_factory() as uow:
            if await uow.users.get_by_email(email) is not None:
                raise UserAlreadyRegisterError("User email already register")

            password_hash = self.password_hasher.hash(raw_password.value)

            user = User.register(
                email=email,
                nickname=nickname,
                password_hash=password_hash,
            )

            await uow.users.add(user)
            await uow.commit()
