from pydantic import BaseModel, constr, validator
from datetime import datetime
from typing import Optional


class PostId(int):
    @classmethod
    def validate(cls, value: int):
        if value < 1:
            raise ValueError("Invalid Post ID")
        return cls(value)


class PostText(constr(min_length=1, max_length=10000)):
    @classmethod
    def validate(cls, text: str):
        if len(text.encode('utf-8')) > 1_000_000:
            raise ValueError("Text exceeds 1MB limit")
        return cls(text)


class Post(BaseModel):
    id: Optional[PostId]
    text: PostText
    user_id: int 
    created_at: datetime

    @classmethod
    def create(cls, text: str, user_id: int) -> 'Post':
        return cls(
            text=PostText.validate(text),
            user_id=user_id,
            created_at=datetime.utcnow()
        )