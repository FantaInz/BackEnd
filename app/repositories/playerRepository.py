from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from app.views.user import UserSchemaCreate
from app.models.player import Player
from app.utils.passwords import get_password_hash
from sqlalchemy.orm import Session

logger = logging.getLogger('uvicorn.error')
def get_player_by_id(player_id: int, db: Session):
    result =db.execute(select(Player).filter(Player.id == player_id))
    player=result.scalars().first()
    return player

def search_players(db: Session, search):
    stmt=select(Player)
    if search.teams:
        stmt=stmt.filter(Player.team_id.in_(search.teams))
    if search.positions:
        stmt=stmt.filter(Player.position.in_(search.positions))
    if search.name:
        stmt=stmt.filter(Player.name.ilike(f"%{search.name}%"))
    if search.minPrice:
        stmt=stmt.filter(Player.price>=search.minPrice)
    if search.maxPrice:
        stmt=stmt.filter(Player.price<=search.maxPrice)

    if search.SortPoints:
        if search.SortPoints.expected:
            stmt=stmt.order_by(Player.expectedPoints[search.SortPoints.gameweek].desc() if search.SortPoints.order=="desc" else Player.expectedPoints[search.SortPoints.gameweek].asc())
        else:
            stmt=stmt.order_by(Player.points[search.SortPoints.gameweek].desc() if search.SortPoints.order=="desc" else Player.points[search.SortPoints.gameweek].asc())
    if search.sortTeam:
        stmt=stmt.order_by(Player.team_id.desc() if search.sortTeam=="desc" else Player.team_id.asc())

    if search.sortPosition:
        stmt=stmt.order_by(Player.position.desc() if search.sortPosition=="desc" else Player.position.asc())

    if search.sortName:
        stmt=stmt.order_by(Player.name.desc() if search.sortName=="desc" else Player.name.asc())
    result = db.execute(stmt)
    players=result.scalars().all()
    cnt=len(players)
    return players[search.pageNumber*search.pageSize:(search.pageNumber+1)*search.pageSize],cnt

def get_all_players( db: Session):
    result = db.execute(select(Player))
    return result.scalars().all()