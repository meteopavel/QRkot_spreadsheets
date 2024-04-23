from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.db import Base


class Investment(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    table__args = (
        CheckConstraint(
            'full_amount > 0',
            name='Значение начальной инвестиции должно быть больше 0'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='Инвестированная сумма должна быть меньше или равна '
                 'полной сумме'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='Инвестированная сумма не должна быть отрицательной'
        )
    )

    def __repr__(self):
        return (f'{type(self).name} #{self.id}: '
                f'Текущая сумма инвестиции: {self.invested_amount}'
                f'/{self.full_amount}. Создано: {self.create_date}, '
                f'Закрыто: {self.close_date}')
