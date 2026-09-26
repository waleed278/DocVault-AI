from pathlib import Path

from fastapi import UploadFile

from app.core.exceptions import (
    FileTooLargeError,
    InvalidFileContentError,
    InvalidFileTypeError,
)


MAX_FILE_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024


ALLOWED_TYPES = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
}


async def validate_uploaded_file(
    file: UploadFile,
) -> int:

    if not file.filename:
        raise InvalidFileTypeError()

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_TYPES:
        raise InvalidFileTypeError()

    expected_content_type = ALLOWED_TYPES[
        extension
    ]

    if file.content_type != expected_content_type:
        raise InvalidFileTypeError()

    total_size = 0
    first_bytes = b""

    while True:
        chunk = await file.read(
            CHUNK_SIZE
        )

        if not chunk:
            break

        if total_size == 0:
            first_bytes = chunk[:1024]

        total_size += len(chunk)

        if total_size > MAX_FILE_SIZE:
            raise FileTooLargeError()

    if total_size == 0:
        raise InvalidFileContentError()

    if (
        extension == ".pdf"
        and b"%PDF-" not in first_bytes
    ):
        raise InvalidFileContentError()

    await file.seek(0)

    return total_size