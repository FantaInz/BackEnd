from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.ext.mutable import MutableList
from app.utils.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from decimal import Decimal
from app.models.team import Team

class Player(Base):
    __tablename__ = 'players'
    id:Mapped[int]= mapped_column(Integer,primary_key=True, autoincrement=True,nullable=False)
    name:str=Column(String,nullable=False)
    team_id:Mapped[int]=mapped_column(ForeignKey('teams.id'))
    team:Mapped["Team"]=relationship(lazy="selectin")
    position:int=Column(Integer,nullable=False)
    price:int=Column(Integer,nullable=False)
    expectedPoints:list[Decimal] = Column(MutableList.as_mutable(ARRAY(DECIMAL(4,2))),nullable=False)
    points:list[int] = Column(MutableList.as_mutable(ARRAY(Integer)),nullable=False)
    availability:int=Column(Integer,nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "team_id": self.team_id,
            "position": self.position,
            "price": self.price,
            "expectedPoints": self.expectedPoints,
            "availability": self.availability
        }

