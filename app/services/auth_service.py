from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError
from app.core.security import (
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:

    statement = select(User).where(
        User.email == email
    )

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def register_user(
    db: AsyncSession,
    user_in: UserCreate,
) -> User:

    email = str(user_in.email).strip().lower()

    existing_user = await get_user_by_email(
        db,
        email,
    )

    if existing_user is not None:
        raise UserAlreadyExistsError()

    hashed_password = await run_in_threadpool(
        hash_password,
        user_in.password,
    )

    user = User(
        email=email,
        hashed_password=hashed_password,
    )

    db.add(user)

    try:
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise UserAlreadyExistsError() from None

    await db.refresh(user)

    return user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:

    user = await get_user_by_email(
        db,
        email.strip().lower(),
    )

    if user is None:
        return None

    valid = await run_in_threadpool(
        verify_password,
        password,
        user.hashed_password,
    )

    if not valid:
        return None

    return user