from app.views.futureSquad import FutureSquadSchema
from app.views.plan import PlanSchema
from app.views.player import PlayerSchema
from fastapi import APIRouter,Depends
from  sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.database import get_db
from app.repositories import playerRepository,teamRepository,squadRepository
from app.views.squad import SquadSchema
from app.services.algorithm import algorithmService
from app.views.optimizerConstrains import OptimizerConstrains
from app.models.user import User
from app.controllers.auth.common import get_current_user
router = APIRouter(prefix="/squad", tags=["squad"])


@router.get("/update/{squad_id}")
def update_squad(squad_id: int, db: Session = Depends(get_db),user=Depends(get_current_user))->SquadSchema:
    squad= squadRepository.update_or_create_squad(squad_id,user, db)
    return SquadSchema.from_model(squad)

@router.post("/optimize")
def optimize_squad(constrains:OptimizerConstrains,db: Session = Depends(get_db),user=Depends(get_current_user))->PlanSchema:
    return algorithmService.optimize_squad(constrains,db,user)

@router.get("/dream_team/{week}")
def get_dream_team(week:int,db: Session = Depends(get_db))->FutureSquadSchema:
    return algorithmService.get_dream_team(db,week)

