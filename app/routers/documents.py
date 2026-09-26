from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    FileTooLargeError,
    InvalidFileContentError,
    InvalidFileTypeError,
    StorageServiceError,
)
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    create_document,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=201,
)
async def upload_document(
    file: Annotated[
        UploadFile,
        File(description="PDF or TXT document"),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        return await create_document(
            db=db,
            current_user=current_user,
            file=file,
        )

    except InvalidFileTypeError:
        raise HTTPException(
            status_code=415,
            detail=(
                "Only PDF and TXT files "
                "are supported"
            ),
        )

    except FileTooLargeError:
        raise HTTPException(
            status_code=413,
            detail="File exceeds 10 MB limit",
        )

    except InvalidFileContentError:
        raise HTTPException(
            status_code=422,
            detail="File content is invalid",
        )

    except StorageServiceError:
        raise HTTPException(
            status_code=503,
            detail="Document storage is unavailable",
        )