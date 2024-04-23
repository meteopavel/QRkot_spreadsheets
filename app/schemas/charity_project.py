from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, StrictInt, PositiveInt

from app.core.constants import MAX_ANYSTR_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=MAX_ANYSTR_LENGTH,
    )
    description: Optional[str] = Field(
        None,
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        max_length=MAX_ANYSTR_LENGTH,
    )
    description: str = Field(...,)
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: StrictInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
