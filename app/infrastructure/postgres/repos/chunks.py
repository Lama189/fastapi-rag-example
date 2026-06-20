from uuid import UUID
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.document_chunk import DocumentChunk as DocumentChunkDomain
from app.infrastructure.postgres.models.document_chunk import DocumentChunk as DocumentChunkModel
from app.application.interfaces.chunks import IChunkRepository


class PostgresChunkRepository(IChunkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_documents(
        self, 
        texts: list[str], 
        embeddings: list[float], 
        metadatas: list[dict[str, object]]
    ) -> None:
        stmt = insert(DocumentChunkModel).values(
            [
                {
                    "content": text,
                    "metadata_": metadata,
                    "embedding": embedding,
                }
                for text, metadata, embedding in zip(texts, metadatas, embeddings, strict=True)
            ]
        )

        await self._session.execute(stmt)
    
    async def find_similar_chunks(
        self,
        embedding: list[str],
        limit: int = 5
    ) -> list[DocumentChunkDomain]:
        stmt = (
            select(DocumentChunkModel)
            .order_by(DocumentChunkModel.embedding.cosine_distance(embedding))
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return [self._to_domain(row) for row in rows]
    
    def _to_domain(self, model: DocumentChunkModel) -> DocumentChunkDomain:
        return DocumentChunkDomain(
            id=model.id,
            content=model.content,
            metadata_=model.metadata_,
            embedding=model.embedding,
            created_at=model.created_at,
        )