from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, StrictInt, Extra


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDBShort(DonationBase):
    id: int
    full_amount: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBFull(DonationDBShort):

    user_id: int
    invested_amount: StrictInt
    fully_invested: bool = False
    close_date: Optional[datetime]
