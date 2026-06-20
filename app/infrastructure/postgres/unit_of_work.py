from types import TracebackType
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.database import async_session_maker

from app.application.interfaces.unit_of_work import IUnitOfWork
from app.infrastructure.postgres.repos.chunks import PostgresChunkRepository


class PostgresUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session

    async def __aenter__(self) -> "PostgresUnitOfWork":
        if self._session is None:
            self._session = async_session_maker()

        self.chunks = PostgresChunkRepository(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            if self._session:
                await self._session.close()

    async def commit(self) -> None:
        if self._session:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session:
            await self._session.rollback()