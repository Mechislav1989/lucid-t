from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


class DataBase:
    def __init__(self, url: str) -> None:
        self._async_engine = create_async_engine(
            url=url,
            pool_pre_ping=True,
            echo=True,
            isolation_level='READ COMMITTED'
        )
        self._async_session = async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=False
        )
        self._session_context: AsyncSession | None = ContextVar(
            "session_context",
            default=None,
        )

    def start_session(self) -> AsyncSession:
        if not self._session_context.get():
            self._session_context.set(self._async_session())
        return self._session_context.get()         

    def get_session(self) -> AsyncSession | None:
        return self._session_context.get()

    @asynccontextmanager
    async def session_context(self):
        session = self._async_session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()