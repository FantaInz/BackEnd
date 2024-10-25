from sqlalchemy import Column, String, select, Integer, ForeignKey
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import Base

class User(Base):
    __tablename__ = 'users'
    id= Column( Integer, primary_key=True, autoincrement=True,nullable=False)
    username = Column( String, unique=True, nullable=False)
    password = Column( String, nullable=False)
    email = Column( String, nullable=False,unique=True)
    team_id = Column( Integer, nullable=True)
