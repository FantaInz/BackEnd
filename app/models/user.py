from sqlalchemy import Column, String, select, Integer, ForeignKey
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import Base

class User(Base):
    __tablename__ = 'users'
    id:int= Column( Integer, primary_key=True, autoincrement=True,nullable=False)
    username:str = Column( String, unique=True, nullable=False)
    password:str = Column( String, nullable=True)
    email:str = Column( String, nullable=False,unique=True)
    squad_id:int = Column( Integer, nullable=True)

