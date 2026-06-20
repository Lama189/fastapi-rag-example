from app.application.interfaces.chunks import IChunkRepository


class IUnitOfWork:
    chunks: IChunkRepository

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...