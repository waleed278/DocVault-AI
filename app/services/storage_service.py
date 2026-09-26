from pathlib import Path
from uuid import uuid4
from fastapi.concurrency import run_in_threadpool
from minio import Minio
from minio.error import S3Error

from app.core.config import settings
from app.core.exceptions import StorageServiceError


storage_client =  Minio(
    settings.storage_endpoint,
    access_key=settings.storage_access_key,
    secret_key=settings.storage_secret_key,
    secure=settings.storage_secure
)

def build_storage_key(
    user_id: int,
    original_filename: str,
) -> str:

    extension = Path(
        original_filename
    ).suffix.lower()

    unique_name = (
        f"{uuid4()}{extension}"
    )

    return (
        f"users/{user_id}/documents/"
        f"{unique_name}"
    )


def ensure_bucket_exists_sync()->None:
    exists = storage_client.bucket_exists(
        settings.storage_bucket
    )

    if not exists:
        storage_client.make_bucket(
            settings.storage_bucket
        )


def upload_object_sync(
        fileobject,
        object_key:str,
        size_bytes:int,
        content_type: str) ->None:
    ensure_bucket_exists_sync()

    storage_client.put_object(
        bucket_name=settings.storage_bucket,
        object_name=object_key,
        data = fileobject,
        length= size_bytes,
        content_type=content_type
    )

async def upload_object(
    file_object,
    object_key: str,
    size_bytes: int,
    content_type: str,
) -> None:

    try:
        await run_in_threadpool(
            upload_object_sync,
            file_object,
            object_key,
            size_bytes,
            content_type,
        )

    except S3Error as exc:
        raise StorageServiceError(
            "Object upload failed"
        ) from exc


def delete_object_sync(
        object_key:str
)->None:

    storage_client.remove_object(
        settings.storage_bucket,
        object_key
    )

async def delete_object(
    object_key: str,
) -> None:

    try:
        await run_in_threadpool(
            delete_object_sync,
            object_key,
        )

    except S3Error as exc:
        raise StorageServiceError(
            "Could not remove stored object"
        ) from exc