import logging

from fastapi import FastAPI


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