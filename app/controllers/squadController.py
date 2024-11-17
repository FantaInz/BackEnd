from app.views.player import PlayerSchema
from fastapi import APIRouter,Depends
from  sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.database import get_db
from app.repositories import playerRepository,teamRepository,squadRepository

router = APIRouter(prefix="/squad", tags=["squad"])

@router.get("/get/players/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db))->PlayerSchema:
    player = playerRepository.get_player_by_id(player_id, db)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerSchema.from_model(player)
@router.get("/get/teams/select/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = teamRepository.get_team_by_id(team_id, db)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
@router.get("/update/{squad_id}")
def update_squad(squad_id: int, db: Session = Depends(get_db)):
    squad= squadRepository.update_or_create_squad(squad_id, db)
    return squad

@router.get("/get/teams/all")
def get_team(db: Session = Depends(get_db)):
    teams = teamRepository.get_teams(db)
    if teams is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams