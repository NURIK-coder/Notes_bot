import datetime

from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, insert, select

from app.base import Base

from app.database import async_session_maker

class Note(Base):
    __tablename__ = 'notes'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)


    @classmethod
    async def create(cls, **data):
        async with async_session_maker()as session:

            query = insert(cls).values(**data).returning(cls)

            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls)
            result = await session.execute(query)
            return result.scalars().all()