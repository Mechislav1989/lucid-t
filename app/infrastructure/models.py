from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from database import Base


class PostORM(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)