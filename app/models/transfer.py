from sqlalchemy import Column, String, Integer,ForeignKey
from app.utils.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from app.models.player import Player
class Transfer(Base):
    __tablename__ = 'transfers'

    id:Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True,nullable=False)
    gameWeek:int = Column(Integer, nullable=False)
    squad_id:Mapped[int]=mapped_column(ForeignKey("squads.id"))
    inPlayerId:Mapped[int]=mapped_column(ForeignKey("players.id"))
    playerIn:Mapped["Player"]=relationship(lazy="selectin",foreign_keys=[inPlayerId])
    outPlayerId:Mapped[int]=mapped_column(ForeignKey("players.id"))
    playerOut:Mapped["Player"]=relationship(lazy="selectin",foreign_keys=[outPlayerId])
    inPlayerPrice:Mapped[int]=Column(Integer,nullable=False)
    outPlayerPrice:Mapped[int]=Column(Integer,nullable=False)


