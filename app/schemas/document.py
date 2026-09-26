from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    id: int
    owner_id: int

    original_filename: str
    content_type: str
    size_bytes: int

    status: DocumentStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )