from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select

from domain.users.model import User, UserId
from infrastructure.database import DataBase


@dataclass
class UserRepository:
    db: DataBase

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.db.session_context() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            db_user = result.scalars().first()
            return self._to_domain(db_user) if db_user else None
        
    def _to_domain(self, db_user: User) -> User:
        return User(
            id=UserId(db_user.id),
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at
        )