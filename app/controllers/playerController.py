from app.views.player import PlayerSchema
from fastapi import APIRouter,Depends
from  sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.database import get_db
from app.repositories import playerRepository
from app.services.algorithm import algorithmService
from app.models.user import User
from app.views.player import PlayerSchema, PlayerSearch,SearchResult
from app.controllers.auth.common import get_current_user
from websockets.http11 import Response

router = APIRouter(prefix="/player", tags=["player"])

@router.post("/search")
def search_players(
    search: PlayerSearch,
    db: Session = Depends(get_db)
)->SearchResult:
    plyrs,cnt=playerRepository.search_players(db, search)
    res=SearchResult()
    res.players=[PlayerSchema.from_model(player) for player in plyrs]
    res.totalPages=cnt//search.pageSize+1
    return res
@router.get("/count",response_model=int)
def get_player_count(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return len(playerRepository.get_all_players(db))