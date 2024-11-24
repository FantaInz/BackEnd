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
    result = db.execute(stmt.offset(search.pageNumber*search.pageSize).limit(search.pageSize))
    return result.scalars().all()

def get_all_players( db: Session):
    result = db.execute(select(Player))
    return result.scalars().all()