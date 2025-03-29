from pydantic import GetCoreSchemaHandler, BaseModel, ConfigDict
from pydantic_core import CoreSchema, core_schema
from datetime import datetime
from typing import Any


class PostId(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.chain_schema(
            [
                handler.generate_schema(int),
                core_schema.general_plain_validator_function(cls.validate),
            ]
        )

    @classmethod
    def validate(cls, value: int) -> 'PostId':
        if not isinstance(value, int) or value < 1:
            raise ValueError("Invalid Post ID")
        return cls(value)


class PostText(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.chain_schema(
            [
                handler.generate_schema(str),  # Генерация схемы для str
                core_schema.general_plain_validator_function(cls.validate),
            ]
        )

    @classmethod
    def validate(cls, v: str) -> 'PostText':
        if len(v.encode('utf-8')) > 1_000_000:
            raise ValueError("Text exceeds 1MB limit")
        return cls(v)


class Post(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: PostId
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
