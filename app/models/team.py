from sqlalchemy import Column, String, Integer
from app.utils.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column


class Team(Base):
    __tablename__ = 'teams'
    name:str = Column(String, nullable=False)
    id:Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True,nullable=False)

