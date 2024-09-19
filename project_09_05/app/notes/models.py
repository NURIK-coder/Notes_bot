import datetime

from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, insert, select, update, delete, ForeignKey
from sqlalchemy.orm import relationship, joinedload

from app.base import Base

from app.database import async_session_maker
from app.users.models import User
class Note(Base):
    __tablename__ = 'notes'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    status = Column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('users.tg_id', ondelete='CASCADE'))
    user = relationship('User', back_populates='notes')
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls).options(joinedload(cls.user))
            result = await session.execute(query)
            return result.scalars().all()



