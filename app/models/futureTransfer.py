from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.ext.mutable import MutableList
from app.utils.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from app.models.player import Player

futureTransfer_playerIn_association=Table(
    "futureTransfer_playerIn",
    Base.metadata,
    Column("futureTransfer_id", Integer, ForeignKey("futureTransfers.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
)
futureTransfer_playerOut_association=Table(
    "futureTransfer_playerOut",
    Base.metadata,
    Column("futureTransfer_id", Integer, ForeignKey("futureTransfers.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
)

class FutureTransfer(Base):
    __tablename__ = 'futureTransfers'
    id:Mapped[int]= mapped_column(Integer,primary_key=True, autoincrement=True,nullable=False)
    plan_id:Mapped[int]=mapped_column(ForeignKey('plans.id'))
    gameweek:int=Column(Integer,nullable=False)
    players_in: Mapped[list["Player"]] = relationship(secondary=futureTransfer_playerIn_association, lazy="selectin")
    players_out: Mapped[list["Player"]] = relationship(secondary=futureTransfer_playerOut_association, lazy="selectin")
