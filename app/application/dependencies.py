from typing import Annotated
from fastapi import Depends
from collections.abc import AsyncGenerator

from app.core.config import get_settings
from app.application.interfaces.unit_of_work import IUnitOfWork
from app.application.services.rag import RagService

from app.infrastructure.postgres.unit_of_work import PostgresUnitOfWork


settings = get_settings()


async def get_uow() -> AsyncGenerator[IUnitOfWork, None]:
    async with PostgresUnitOfWork() as uow:
        yield uow


async def get_rag_service(uow: Annotated[IUnitOfWork, Depends(get_uow)]) -> RagService:
    return RagService(uow)