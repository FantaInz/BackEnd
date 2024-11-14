from sqlalchemy import Column, String, select, Integer, ForeignKey,Numeric,ARRAY
from sqlalchemy.ext.mutable import MutableList
from app.services.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from decimal import Decimal
from app.models.team import Team

class Player(Base):
    __tablename__ = 'players'
    id:Mapped[int]= mapped_column(Integer,primary_key=True, autoincrement=True,nullable=False)
    name:str=Column(String,nullable=False)
    team_id:Mapped[int]=mapped_column(ForeignKey('teams.id'))
    team:Mapped["Team"]=relationship()
    position:str=Column(String,nullable=False)
    price:int=Column(Integer,nullable=False)
    expectedPoints:list[int] = Column(MutableList.as_mutable(ARRAY(Integer)),nullable=False)
    points:list[int] = Column(MutableList.as_mutable(ARRAY(Integer)),nullable=False)
    availability:int=Column(Integer,nullable=False)

