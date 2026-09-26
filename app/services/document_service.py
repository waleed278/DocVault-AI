from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import StorageServiceError
from app.core.config import settings
from app.models.user import User
from app.models.document import Document,DocumentStatus
from app.services.file_validation_service import validate_uploaded_file
from app.services.storage_service import build_storage_key,delete_object,upload_object

async def create_document(
        db:AsyncSession,
        current_user:User,
        file:UploadFile)->Document:
    size_bytes = await validate_uploaded_file(
        file
    )
    object_key = build_storage_key(
        current_user.id,
        file.filename
    )
    await file.seek(0)

    await upload_object(
        file_object=file.file,
        object_key=object_key,
        size_bytes=size_bytes,
        content_type=(file.content_type or "application/octet-stream"),
    )

    document = Document(
        owner_id=current_user.id,
        original_filename=file.filename,
        content_type=(
            file.content_type
            or "application/octet-stream"
        ),
        size_bytes=size_bytes,
        storage_bucket=settings.storage_bucket,
        storage_key=object_key,
        status=DocumentStatus.UPLOADED,
    )

    db.add(document)

    try:
        await db.commit()

    except SQLAlchemyError:
        await db.rollback()

        try:
            await delete_object(
                object_key
            )
        except StorageServiceError:
            pass
        raise

    await db.refresh(document)

    return document