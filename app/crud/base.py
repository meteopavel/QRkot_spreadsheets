from typing import TypeVar, Optional, List, Generic, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[CreateSchemaType, ModelType, UpdateSchemaType]):

    def __init__(self, model):
        self.model = model

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None,
        skip_commit: bool = False,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        if (hasattr(db_obj, 'invested_amount') and
                db_obj.invested_amount is None):
            db_obj.invested_amount = 0
        session.add(db_obj)
        if not skip_commit:
            return await self.add_to_database(db_obj, session)
        return db_obj

    async def patch(
        self,
        db_obj: ModelType,
        input_data_obj: UpdateSchemaType,
        session: AsyncSession,
        skip_commit: bool = False,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = input_data_obj.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if not skip_commit:
            return await self.add_to_database(db_obj, session)
        return db_obj

    @staticmethod
    async def delete(db_obj: ModelType, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def add_to_database(obj: Base, session: AsyncSession) -> ModelType:
        await session.commit()
        await session.refresh(obj)
        return obj

    async def get_unclosed_projects(
        self, session: AsyncSession
    ) -> Union[List[ModelType], ModelType]:
        """
        Получить благотворительные проекты, для которых не задан параметр
        close_date
        """
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.close_date.is_(None))
            .order_by(asc('create_date'))
        )
        return db_objs.scalars().all()

    async def get_closed_projects(
        self, session: AsyncSession
    ) -> Union[List[ModelType], ModelType]:
        """
        Получить благотворительные проекты, для которых задан параметр
        close_date
        """
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.close_date.is_not(None))
            .order_by(asc('create_date'))
        )
        return db_objs.scalars().all()





    # async def get_closed_projects(
    #         self,
    #         from_reserve: datetime,
    #         to_reserve: datetime,
    #         session: AsyncSession,
    # ) -> list[dict[str, int]]:
    #     reservations = await session.execute(
    #         # Получаем количество бронирований переговорок за период
    #         select([Reservation.meetingroom_id,
    #                 func.count(Reservation.meetingroom_id)]).where(
    #             Reservation.from_reserve >= from_reserve,
    #             Reservation.to_reserve <= to_reserve
    #         ).group_by(Reservation.meetingroom_id)
    #     )
    #     reservations = reservations.all()
    #     return reservations