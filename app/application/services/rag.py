import asyncio
from fastapi import UploadFile
from langchain_core.document_loaders import Blob

from app.application.exceptions.rag import RagContentTypeException
from app.domain.document_chunk import DocumentChunk

from app.application.interfaces.unit_of_work import IUnitOfWork
from app.infrastructure.ai.chain.ollama import chain
from app.infrastructure.ai.documents.parser import pdf_parser
from app.infrastructure.ai.documents.splitter import splitter
from app.infrastructure.ai.embeddings.hf import hf_embeddings
from app.infrastructure.logging.decorators import log_duration

BATCH_SIZE = 5  
DELAY = 1.0   


class RagService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    @log_duration
    async def upload_pdf(self, file: UploadFile) -> None:
        if file.content_type != "application/pdf":
            raise RagContentTypeException
        
        file_bytes = await file.read()
        blob = Blob.from_data(file_bytes, mime_type="application/pdf")
        documents = pdf_parser.parse(blob)
        for doc in documents:
            doc.metadata["filename"] = file.filename

        document_chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in document_chunks]
        
        embeddings = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            
            batch_embeddings = await hf_embeddings.aembed_documents(batch)
            embeddings.extend(batch_embeddings)
            
            if i + BATCH_SIZE < len(texts):
                await asyncio.sleep(DELAY)

        metadatas = [chunk.metadata for chunk in document_chunks]

        await self._uow.chunks.add_documents(texts, embeddings, metadatas)
        await self._uow.commit()


    @log_duration
    async def ask_pdf(self, query: str) -> str:
        embedding = await hf_embeddings.aembed_query(query)
        chunks = await self._uow.chunks.find_similar_chunks(embedding)

        context = "\n\n".join(chunk.content for chunk in chunks)
        response = await chain.ainvoke(
            {
                "context": context,
                "query": query
            }
        )

        return response