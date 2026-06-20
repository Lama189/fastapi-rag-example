from typing import Annotated
from fastapi import APIRouter, Depends, Query, UploadFile, File
from starlette import status

from app.application.services.rag import RagService
from app.application.dto.rag import UploadResponse
from app.application.dependencies import get_rag_service


router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post(
    path="/upload/pdf",
    status_code=status.HTTP_201_CREATED
)
async def upload_pdf(
    service: Annotated[RagService, Depends(get_rag_service)],
    files: list[UploadFile] = File(...),
):
    for file in files:
        await service.upload_pdf(file)

    return UploadResponse(
        filenames=[f.filename for f in files]
    )


@router.get(
    path="/ask-pdf",
    status_code=status.HTTP_200_OK
)
async def ask_pdf(
    query: Annotated[str, Query(min_length=1)],
    service: Annotated[RagService, Depends(get_rag_service)]
):
    return await service.ask_pdf(query)