from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: str = "success"
    filenames: list[str]