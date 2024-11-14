from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.services.database import get_db
from app.repositories import playerRepository
from app.views.user import UserSchema,UserSchemaCreate

router = APIRouter(prefix="/squad", tags=["squad"])

@router.get("/get/{player_id}")
async def get_player(player_id: int, db: AsyncSession = Depends(get_db)):
    player = await playerRepository.get_player_by_id(player_id, db)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player