from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY

from app.utils.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from app.models.player import Player
from app.models.futureTransfer import FutureTransfer
from app.models.futureSquad import FutureSquad

class Plan(Base):

    __tablename__ = 'plans'
    id:Mapped[int]= mapped_column(Integer,primary_key=True, autoincrement=True,nullable=False)
    name:str = Column(String,nullable=False)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    squad_id:Mapped[int]=mapped_column(ForeignKey('squads.id'))
    start_gameweek:int=Column(Integer,nullable=False)
    end_gameweek:int=Column(Integer,nullable=False)
    futureTransfers: Mapped[list["FutureTransfer"]] = relationship(lazy="selectin")
    futureSquads: Mapped[list["FutureSquad"]] = relationship(lazy="selectin")
