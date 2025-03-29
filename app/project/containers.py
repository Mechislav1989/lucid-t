from functools import lru_cache
from cachetools import TTLCache
from fastapi import Security
import punq

from application.posts.use_cases import CreatePostUseCase, DeletePostUseCase, GetPostsUseCase
from application.users.use_cases import LoginUseCase, SignupUseCase
from infrastructure.caching import PostCache
from infrastructure.database import DataBase
from infrastructure.repositories.posts import PostRepository
from infrastructure.repositories.users import UserRepository
from project.general import settings


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()
    
    container.register(
        DataBase,
        scope=punq.Scope.singleton,
        factory=lambda: DataBase(
            url=settings.DB_URL_asyncpg,
        ),
    )
    
    container.register(
        UserRepository, 
        factory=UserRepository(db=container.resolve(DataBase)), scope=punq.Scope.singleton
    )
    container.register(
        PostRepository,
        factory=PostRepository(db=container.resolve(DataBase)), scope=punq.Scope.singleton
    )
    container.register(
        PostCache,
        factory=PostCache(cache=TTLCache(maxsize=1000, ttl=300)), scope=punq.Scope.singleton
    )
    container.register(
        CreatePostUseCase, 
        factory=CreatePostUseCase, 
        scope=punq.Scope.singleton
    )
    container.register(
        Security, factory=Security(settings.SECRET_KEY, settings.ALGORITHM), scope=punq.Scope.singleton
        )
    
    container.register(
        SignupUseCase, 
        factory=SignupUseCase(user_repo=container.resolve(UserRepository)), 
        scope=punq.Scope.singleton
    )
    container.register(
        LoginUseCase, 
        factory=LoginUseCase(user_repo=container.resolve(UserRepository), security=container.resolve(Security)),
        scope=punq.Scope.singleton
    )
    container.register(
        CreatePostUseCase, 
        factory=CreatePostUseCase(
            post_repo=container.resolve(PostRepository), 
            user_repo=container.resolve(UserRepository), 
            cache=container.resolve(PostCache)
        ),
        scope=punq.Scope.singleton
    )
    container.register(
        GetPostsUseCase, 
        factory=GetPostsUseCase(post_repo=container.resolve(PostRepository), cache=container.resolve(PostCache)),
        scope=punq.Scope.singleton
    )
    container.register(
        DeletePostUseCase, 
        factory=DeletePostUseCase(post_repo=container.resolve(PostRepository), cache=container.resolve(PostCache)),
        scope=punq.Scope.singleton
    )
    return container
