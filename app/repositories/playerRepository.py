from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.views.user import UserSchemaCreate
from app.models.player import Player
from app.utils.passwords import get_password_hash


async def get_player_by_id(player_id: int, db: AsyncSession):
    result = await db.execute(select(Player).filter(Player.id == player_id))
    return result.scalars().first()