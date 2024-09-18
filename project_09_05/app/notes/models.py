import datetime

from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, insert, select, update, delete

from app.base import Base

from app.database import async_session_maker

class Note(Base):
    __tablename__ = 'notes'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)


