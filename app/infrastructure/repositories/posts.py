from dataclasses import dataclass

from sqlalchemy import select

from domain.posts.model import Post
from infrastructure.database import DataBase
from infrastructure.models import PostORM


@dataclass
class PostRepository:
    db: DataBase

    async def save(self, post: Post) -> Post:
        async with self.db.session_context() as session:
            db_post = PostORM(
                text=post.text,
                user_id=post.user_id,
                created_at=post.created_at
            )
            session.add(db_post)
            await session.commit()
            await session.refresh(db_post)
            return self._to_domain(db_post)

    async def get_by_user(self, user_id: int) -> list[Post]:
        async with self.db.session_context() as session:
            result = await session.execute(
                select(PostORM).where(PostORM.user_id == user_id)
            )
            db_posts = result.scalars().all()
            return [self._to_domain(p) for p in db_posts]

    def _to_domain(self, db_post) -> Post:
        """Mapping ORM -> Domain Model"""
        return Post(
            id=db_post.id,
            text=db_post.text,
            user_id=db_post.user_id,
            created_at=db_post.created_at
        )