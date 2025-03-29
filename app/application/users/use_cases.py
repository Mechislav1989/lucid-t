from dataclasses import dataclass
from domain.users.model import User
from infrastructure.repositories.users import UserRepository


@dataclass
class SignupUseCase:
    user_repo: UserRepository

    async def execute(self, email: str, password: str) -> User:
        if await self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")
        
        user = User.create(email, password)
        await self.user_repo.save(user)
        return user