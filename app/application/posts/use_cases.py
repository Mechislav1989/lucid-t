from dataclasses import dataclass
from typing import List

from domain.posts.model import Post
from domain.posts.service import PostService
from infrastructure.caching import PostCache
from infrastructure.repositories.posts import PostRepository
from infrastructure.repositories.users import UserRepository


@dataclass
class CreatePostUseCase:
    post_repo: PostRepository
    user_repo: UserRepository
    cache: PostCache

    async def execute(self, text: str, user_id: int) -> Post:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if not PostService.validate_post_content(text):
            raise ValueError("Post contains forbidden content")

        post = Post.create(text, user_id)
        saved_post = await self.post_repo.save(post)
        self.cache.invalidate(user_id)
        return saved_post


@dataclass
class GetPostsUseCase:
    post_repo: PostRepository
    cache: PostCache

    async def execute(self, user_id: int) -> List[Post]:
        if cached := self.cache.get(user_id):
            return cached
        posts = await self.post_repo.get_by_user(user_id)
        self.cache.set(user_id, posts)
        return posts


@dataclass
class DeletePostUseCase:
    post_repo: PostRepository
    cache: PostCache

    async def execute(self, post_id: int, user_id: int) -> bool:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        if post.user_id != user_id:
            raise ValueError("You are not allowed to delete this post")
        
        await self.post_repo.delete(post_id)
        self.cache.invalidate(user_id)
        return True