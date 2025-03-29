from pydantic import BaseModel
from datetime import datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PostCreateRequest(BaseModel):
    text: str


class PostResponse(BaseModel):
    id: int
    text: str
    user_id: int
    created_at: datetime


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime