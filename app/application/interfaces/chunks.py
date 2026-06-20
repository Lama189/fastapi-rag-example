from abc import ABC, abstractmethod

from app.domain.document_chunk import DocumentChunk


class IChunkRepository(ABC):

    @abstractmethod
    async def add_documents(
        self, 
        texts: list[str], 
        embeddings: list[float], 
        metadatas: list[dict[str, object]]
    ) -> None:
        raise NotImplementedError
    

    @abstractmethod
    async def find_similar_chunks(
        self,
        embedding: list[str],
        limit: int = 5
    ) -> list[DocumentChunk]:
        raise NotImplementedError