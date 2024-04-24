from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectUpdate, CharityProjectCreate,
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    @staticmethod
    async def get_project_id_by_name(
        proj_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Получить id проекта по его имени."""
        project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == proj_name)
        )
        return project_id.scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession
    ) -> list[tuple[str]]:
        """
        Получить благотворительные проекты, для которых задан параметр
        close_date. Отсортировать по количеству времени, которое понадобилось
        на сбор средств, — от меньшего к большему.
        """
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    (
                        func.JULIANDAY(CharityProject.close_date) -
                        func.JULIANDAY(CharityProject.create_date)
                    ).label('comp_rate'),
                    CharityProject.description,
                ]
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by('comp_rate')
        )
        return projects.all()


charity_crud = CRUDCharityProject(CharityProject)
