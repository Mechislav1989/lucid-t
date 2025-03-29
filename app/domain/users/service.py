from typing import Optional
from .model import User


class UserService:
    @staticmethod
    def is_email_available(user_repo, email: str) -> bool:
        existing_user = user_repo.get_by_email(email)
        return existing_user is None

    @classmethod
    def register_user(cls, user_repo, email: str, password: str) -> 'User':
        if not cls.is_email_available(user_repo, email):
            raise ValueError("Email already registered")
        return User.create(email, password)