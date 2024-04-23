from typing import Optional

from sqlalchemy import select
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


charity_crud = CRUDCharityProject(CharityProject)
