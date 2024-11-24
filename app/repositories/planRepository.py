from sqlalchemy import select
from app.views.plan import PlanSchema, PlanSchemaList
from app.models.player import Player
from app.models.user import User
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.models.futureSquad import FutureSquad
from app.models.futureTransfer import FutureTransfer
def save_plan(db: Session, plan: PlanSchema,user:User):
    plan.user_id=user.id
    if user.squad_id is None:
        raise HTTPException(status_code=404,detail="User has no squad")
    plan.squad_id=user.squad_id
    plan_model = Plan(
        user_id=plan.user_id,
        name=plan.name,
        squad_id=plan.squad_id,
        start_gameweek=plan.start_gameweek,
        end_gameweek=plan.end_gameweek
    )
    for future_transfer in plan.transfers:
        future_transfer_model = FutureTransfer(
            plan_id=plan_model.id,
            gameweek=future_transfer.gameweek
        )
        for player in future_transfer.transfer_in:
            player_model = db.execute(select(Player).filter(Player.id == player.id)).scalars().first()
            future_transfer_model.players_in.append(player_model)
        for player in future_transfer.transfer_out:
            player_model = db.execute(select(Player).filter(Player.id == player.id)).scalars().first()
            future_transfer_model.players_out.append(player_model)
        plan_model.futureTransfers.append(future_transfer_model)
    for future_squad in plan.squads:
        future_squad_model = FutureSquad(
            plan_id=plan_model.id,
            gameweek=future_squad.gameweek,
            estimatedPoints=future_squad.estimated_points
        )
        for player in future_squad.team:
            player_model=db.execute(select(Player).filter(Player.id==player.id)).scalars().first()
            future_squad_model.team.append(player_model)
        for player in future_squad.subs:
            player_model=db.execute(select(Player).filter(Player.id==player.id)).scalars().first()
            future_squad_model.subs.append(player_model)
        future_squad_model.captain=db.execute(select(Player).filter(Player.id==future_squad.captain.id)).scalars().first()
        plan_model.futureSquads.append(future_squad_model)

    db.add(plan_model)
    db.commit()
    db.refresh(plan_model)
    return plan_model

def get_plan_by_id(db: Session, plan_id: int,user:User):
    result = db.execute(select(Plan).filter(Plan.id == plan_id))

    plan = result.scalars().first()
    if plan is None:
        raise HTTPException(status_code=404,detail="Plan not found")
    if user.id != plan.user_id:
        raise HTTPException(status_code=403,detail="Plan doesnt belong to user")
    return plan

def delete_plan(db: Session, plan_id: int,user:User):
    plan = get_plan_by_id(db, plan_id,user)
    for future_transfer in plan.futureTransfers:
        db.delete(future_transfer)
    for future_squad in plan.futureSquads:
        db.delete(future_squad)
    db.delete(plan)
    db.commit()
    return

def get_my_plans(db: Session,user:User):

    result = db.execute(select(Plan).filter(Plan.user_id == user.id)
                        .filter(Plan.squad_id == user.squad_id))
    plans = result.scalars().all()
    return [PlanSchemaList.from_model(model) for model in plans]