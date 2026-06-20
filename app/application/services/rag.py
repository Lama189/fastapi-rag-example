from fastapi import UploadFile
from langchain_core.document_loaders import Blob

from app.application.exceptions.rag import RagContentTypeException
from app.domain.document_chunk import DocumentChunk

from app.application.interfaces.unit_of_work import IUnitOfWork
from app.infrastructure.ai.chain.ollama import chain
from app.infrastructure.ai.documents.parser import pdf_parser
from app.infrastructure.ai.documents.splitter import splitter
from app.infrastructure.ai.embeddings.google import google_embeddings


class RagService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    async def upload_pdf(self, file: UploadFile) -> None:
        if file.content_type != "application/json":
            raise RagContentTypeException
        
        file_bytes = await file.read()
        blob = Blob.from_data(file_bytes, mime_type="application/pdf")
        documents = pdf_parser.parse(blob)
        for doc in documents:
            doc.metadata["filename"] = file.filename

        document_chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in document_chunks]
        embeddings = await google_embeddings.aembed_documents(texts)
        metadatas = [chunk.metadata for chunk in document_chunks]

        await self._uow.chunks.add_documents(texts, embeddings, metadatas)
        await self._uow.commit()

    async def ask_pdf(self, query: str) -> str:
        embedding = await google_embeddings.aembed_query(query)
        chunks = await self._uow.chunks.find_similar_chunks(embedding)

        context = "\n\n".join(chunk.content for chunk in chunks)
        response = await chain.ainvoke(
            {
                "context": context,
                "query": query
            }
        )

        return response