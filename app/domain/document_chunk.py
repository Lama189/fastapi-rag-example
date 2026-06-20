from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class DocumentChunk:
    content: str
    metadata_: dict[str, object]
    embedding: list[float]
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
