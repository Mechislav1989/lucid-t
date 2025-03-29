from dataclasses import dataclass
from cachetools import TTLCache


@dataclass
class PostCache:
    cache: TTLCache  # (maxsize=1000, ttl=300)

    def get(self, user_id: int) -> list[dict]:
        return self.cache.get(user_id)

    def set(self, user_id: int, posts: list[dict]):
        self.cache[user_id] = posts

    def invalidate(self, user_id: int):
        if user_id in self.cache:
            del self.cache[user_id]
