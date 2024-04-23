from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_name_is_busy(
    name: str, session: AsyncSession
) -> None:
    """
    Проверить, не занято ли имя благотворительного проекта.
    """
    project_id = await charity_crud.get_project_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'Проект с таким именем уже существует!'
        )


async def check_project_has_investment(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Проверить, не внесены ли средства в благотворительный проект.
    """
    project: CharityProject = await charity_crud.get(project_id, session)
    if project is None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Not found')
    if project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_possibility_for_patching(
    project_id, data_in: CharityProjectUpdate, session: AsyncSession
) -> CharityProject:
    """
    Проверить, возможно ли изменение благотворительного проекта.
    """
    project: CharityProject = await charity_crud.get(project_id, session)
    if project is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Not found')
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'Нельзя изменять полностью проинвестированый'
            'благотворительный проект.'
        )
    if data_in.full_amount and data_in.full_amount < project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'Нелья установить значение full_amount меньше уже вложенной суммы.'
        )
    if data_in.name != project.name:
        await check_project_name_is_busy(data_in.name, session)
    return project
