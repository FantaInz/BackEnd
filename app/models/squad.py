from sqlalchemy import Column, Integer, ForeignKey, Table,String
from app.utils.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from app.models.player import Player
from app.models.transfer import Transfer

squad_player_association=Table(
    "squad_player",
    Base.metadata,
    Column("squad_id", Integer, ForeignKey("squads.id")),
    Column("player_id", Integer, ForeignKey("players.id"))
)
class Squad(Base):
    __tablename__ = "squads"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name:str=Column(String, nullable=False)
    transferBudget:int= Column(Integer, nullable=False)
    freeTransfers:int= Column(Integer, nullable=False)
    lastUpdate:int=Column(Integer, nullable=False)
    players:Mapped[list["Player"]]=relationship(secondary=squad_player_association,lazy="selectin")
    transfers:Mapped[list["Transfer"]]=relationship(lazy="selectin")
