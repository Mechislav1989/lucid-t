from domain.posts.model import Post

class PostService:
    """Сервис для операций с постами"""
    
    @staticmethod
    def can_user_delete_post(post: 'Post', user_id: int) -> bool:
        return post.user_id == user_id

    @staticmethod
    def validate_post_content(text: str) -> bool:
        """Проверка контента на спам/запрещенные слова"""
        forbidden_words = ["spam", "реклама"]
        return not any(word in text.lower() for word in forbidden_words)