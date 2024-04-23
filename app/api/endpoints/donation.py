from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud, charity_crud
from app.models import Donation, User
from app.schemas.donation import (
    DonationDBShort, DonationDBFull, DonationCreate,
)
from app.services.investments import process_investments

router = APIRouter()


@router.get(
    '/', response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех пожертвований. Только для суперпользователей.
    """
    return await donation_crud.get_all(session)


@router.post(
    '/', response_model=DonationDBShort, response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Donation:
    """
    Сделать пожертвование. Только для аутентифицированных пользователей.
    """
    donation = await donation_crud.create(donation, session, user)
    unclosed = await charity_crud.get_unclosed_projects(session)
    if unclosed:
        invested = process_investments(donation, unclosed)
        session.add_all(invested)
    await donation_crud.add_to_database(donation, session)
    return donation


@router.get(
    '/my', response_model=list[DonationDBShort],
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[Donation]:
    """
    Получить список своих пожертвований. Только для аутентифицированных
    пользователей.
    """
    return await donation_crud.get_user_donations(user, session)
