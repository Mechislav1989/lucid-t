from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from infrastructure.security import Security


class UserId(int):
    """Value Object"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, value: int):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Invalid User ID")
        return cls(value)


class User(BaseModel):
    id: Optional[UserId]
    email: EmailStr
    hashed_password: str
    created_at: datetime

    def verify_password(self, password: str) -> bool:
        return Security.pwd_context.verify(password, self.hashed_password)

    @classmethod
    def create(cls, email: str, password: str) -> 'User':
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        return cls(
            email=email,
            hashed_password=Security.pwd_context.hash(password),
            created_at=datetime.utcnow()
        )

    @field_validator('email')
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v