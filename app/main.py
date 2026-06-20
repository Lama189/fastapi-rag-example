import logging


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from app.application.exceptions.rag import RagContentTypeException

from app.api.v1.routers.rag import router as rag_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="RAG example")


@app.get("/")
async def root():
    return {
        "message": "RAG API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.exception_handler(RagContentTypeException)
async def rag_context_type_handler(req: Request, exc: RagContentTypeException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid file format. Only PDF documents are allowed."}
    )


app.include_router(rag_router)