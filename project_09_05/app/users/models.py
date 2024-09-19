from sqlalchemy import Column, Integer, String, select, BigInteger
from sqlalchemy.orm import relationship, joinedload

from app.base import Base
from app.database import async_session_maker


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(100))
    role = Column(String(20))
    phone = Column(String(13))
    notes = relationship('Note', back_populates='user')

    # @classmethod
    # async def get_all(cls):
    #     async with async_session_maker() as session:
    #         query = select(cls).options(joinedload(cls.notes))
    #         result = await session.execute(query)
    #         return result.scalars().all()

    @classmethod
    async def detail(cls, record_id: int):
        async with async_session_maker()as session:
            query = select(cls).filter_by(tg_id=record_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
