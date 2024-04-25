from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_crud

from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """
    Составить отчёт по благотворительным проектам в Google-таблице.
    Только для суперюзеров.
    """
    projects = await charity_crud.get_projects_by_completion_rate(session)
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(
        wrapper_services, projects
    )
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id, wrapper_services, projects
    )
    return {'report_url': spreadsheet_url}
