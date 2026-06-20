from types import TracebackType
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.database import async_session_maker

from app.application.interfaces.unit_of_work import IUnitOfWork


class PostgresUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session