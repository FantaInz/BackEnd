from app.views.plan import PlanSchema, PlanSchemaList
from app.views.player import PlayerSchema
from fastapi import APIRouter,Depends
from  sqlalchemy.orm import Session
from fastapi import HTTPException

from app.utils.database import get_db
from app.repositories import planRepository
from app.models.user import User
from app.controllers.auth.common import get_current_user

router = APIRouter(prefix="/plan", tags=["plan"])

@router.get("/my_plans")
def get_user_plans(db: Session = Depends(get_db),user=Depends(get_current_user))->list[PlanSchemaList]:
    return planRepository.get_my_plans(db,user)

@router.post("/save")
def save_plan(plan:PlanSchema,db: Session = Depends(get_db),user=Depends(get_current_user))->PlanSchema:
    plan_mod=planRepository.save_plan(db,plan,user)
    return PlanSchema.from_model(plan_mod)
@router.delete("/delete/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db),user=Depends(get_current_user))->None:
    planRepository.delete_plan(db,plan_id,user)
    return
@router.get("/get/{plan_id}")
def get_plan(plan_id: int, db: Session = Depends(get_db),user=Depends(get_current_user))->PlanSchema:
    plan_mod=planRepository.get_plan_by_id(db,plan_id,user)
    return PlanSchema.from_model(plan_mod)
