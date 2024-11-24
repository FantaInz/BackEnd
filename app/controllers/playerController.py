from app.views.player import PlayerSchema
from fastapi import APIRouter,Depends
from  sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.database import get_db
from app.repositories import playerRepository
from app.services.algorithm import algorithmService
from app.models.user import User
from app.views.player import PlayerSchema, PlayerSearch
from app.controllers.auth.common import get_current_user
router = APIRouter(prefix="/player", tags=["player"])

@router.post("/search", response_model=list[PlayerSchema])
def search_players(
    search: PlayerSearch,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    players=playerRepository.search_players(db, search)
    return [PlayerSchema.from_model(player) for player in players]