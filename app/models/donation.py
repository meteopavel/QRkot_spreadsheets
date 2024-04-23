from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.base import Investment


class Donation(Investment):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (f'{super().__repr__()},'
                f' Id Пользователя: {self.user_id}, '
                f' Комментарий: {self.comment}')
