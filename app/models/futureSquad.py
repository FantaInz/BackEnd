from sqlalchemy import Column, String, Integer, ForeignKey, Table,DECIMAL
from decimal import Decimal
from app.utils.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from app.models.player import Player

futureSquad_team_association=Table(
    "futureSquad_team",
    Base.metadata,
    Column("futureSquad_id", Integer, ForeignKey("futureSquads.id")),
    Column("player_id", Integer, ForeignKey("players.id"))
)
futureSquad_subs_association=Table(
    "futureSquad_subs",
    Base.metadata,
    Column("futureSquad_id", Integer, ForeignKey("futureSquads.id")),
    Column("player_id", Integer, ForeignKey("players.id"))
)
class FutureSquad(Base):
    __tablename__ = 'futureSquads'
    id:Mapped[int]= mapped_column(Integer,primary_key=True, autoincrement=True,nullable=False)
    plan_id:Mapped[int]=mapped_column(ForeignKey('plans.id'))
    gameweek:int=Column(Integer,nullable=False)
    estimatedPoints:Decimal=Column(DECIMAL(4,2),nullable=False)
    team: Mapped[list["Player"]] = relationship(secondary=futureSquad_team_association, lazy="selectin")
    subs: Mapped[list["Player"]] = relationship(secondary=futureSquad_subs_association, lazy="selectin")
    captain_id:Mapped[int]=mapped_column(ForeignKey('players.id'))
    captain:Mapped["Player"]=relationship(lazy="selectin",foreign_keys=[captain_id])
