from fastapi import FastAPI

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.documents import (
    router as documents_router,
)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(documents_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok"
    }