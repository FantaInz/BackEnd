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

def get_all_players( db: Session):
    result = db.execute(select(Player))
    return result.scalars().all()