from dataclasses import dataclass
from domain.users.model import User
from infrastructure.repositories.users import UserRepository
from infrastructure.security import Security


@dataclass
class SignupUseCase:
    user_repo: UserRepository

    async def execute(self, email: str, password: str) -> User:
        if await self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")
        
        user = User.create(email, password)
        await self.user_repo.save(user)
        return user


@dataclass
class LoginUseCase:
    user_repo: UserRepository
    security: Security

    async def execute(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user or not self.security.verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        return user
