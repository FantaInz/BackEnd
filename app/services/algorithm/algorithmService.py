from app.models.transfer import Transfer
from app.views.plan import PlanSchema
from app.views.transfer import TransferSchema
from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select
import requests
from app.models.squad import Squad,Player
from fastapi import HTTPException
from app.services.algorithm.utils import encode_squad,create_players_dataframe,decode_decision_array
from app.services.algorithm.solver import Solver
from app.views.optimizerConstrains import OptimizerConstrains
from app.views.futureSquad import FutureSquadSchema
from app.views.futureTransfer import FutureTransferSchema
from app.views.player import PlayerSchema
from decimal import Decimal

def get_dream_team(db:Session,week):
    result = db.execute(select(Player).order_by(Player.id))
    players = result.scalars().all()
    df = create_players_dataframe(players, Squad())
    playersNum = len(players)
    solver=Solver(df,None,playersNum,1000,None,1,None)
    try:
        status,squad,team,captain,subs=solver.get_best_squad(week)
    except IndexError:
        raise HTTPException(status_code=400,detail="data for this week is not available")
    if status!=1:
        raise HTTPException(status_code=500,detail="Optimization failed")
    return decode_future_squad(db,team,captain,subs,playersNum,-1,week)

def optimize_squad(constrains:OptimizerConstrains,db:Session,user:User):
    squad_id=user.squad_id
    if squad_id is None:
        raise HTTPException(status_code=404,detail="User has no squad")

    result = db.execute(select(Squad).filter(Squad.id == squad_id))
    squad_obj = result.scalars().first()
    result=db.execute(select(Player).order_by(Player.id))
    players=result.scalars().all()
    df=create_players_dataframe(players,squad_obj)
    playersNum=len(players)
    current_squad=encode_squad(playersNum,squad_obj)
    solver=Solver(df,current_squad,len(players),squad_obj.transferBudget,squad_obj.freeTransfers,constrains.weeks,
                  squad_obj.lastUpdate)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = (
        solver.solve(constrains.must_have,constrains.cant_have))
    if status!=1:
        raise HTTPException(status_code=500,detail="Optimization failed, probably due to unfeasible constraints")
    return get_planSchema(db,squad_obj,team,transfer_in,transfer_out,captain,subs,constrains.weeks,playersNum,
                          squad_obj.lastUpdate)


def decode_future_squad(db,team,captain,subs,playerNum,week,currentWeek):
    future_squad = FutureSquadSchema()
    future_squad.estimated_points = Decimal(0)
    future_squad.gameweek = currentWeek + week + 1
    fteam = decode_decision_array(team, playerNum)
    f_player_obj = db.execute(select(Player).filter(Player.id.in_(fteam))).scalars().all()
    future_squad.team = [PlayerSchema.from_model(player) for player in f_player_obj]
    fsubs = decode_decision_array(subs, playerNum)
    f_subs_obj = db.execute(select(Player).filter(Player.id.in_(fsubs))).scalars().all()
    future_squad.subs = [PlayerSchema.from_model(player) for player in f_subs_obj]
    fcaptain = decode_decision_array(captain, playerNum)
    f_captain_obj = db.execute(select(Player).filter(Player.id.in_(fcaptain))).scalars().first()
    future_squad.captain = PlayerSchema.from_model(f_captain_obj)
    future_squad.estimated_points += sum([player.expectedPoints[week + currentWeek] for player in f_player_obj])
    future_squad.estimated_points += f_captain_obj.expectedPoints[week + currentWeek]
    return future_squad

def decode_future_transfer(db,transfer_in,transfer_out,playerNum,week,currentWeek):
    future_transfer = FutureTransferSchema()
    future_transfer.gameweek = currentWeek + week + 1
    f_transfer_in = decode_decision_array(transfer_in, playerNum)
    f_transfer_in_obj = db.execute(select(Player).filter(Player.id.in_(f_transfer_in))).scalars().all()
    future_transfer.transfer_in = [PlayerSchema.from_model(tran_in) for tran_in in f_transfer_in_obj]

    f_transfer_out = decode_decision_array(transfer_out, playerNum)
    f_transfer_out_obj = db.execute(select(Player).filter(Player.id.in_(f_transfer_out))).scalars().all()
    future_transfer.transfer_out = [PlayerSchema.from_model(tran_out) for tran_out in f_transfer_out_obj]
    return future_transfer

def get_planSchema(db,squad_obj,team,transfer_in,transfer_out,captain,subs,weeks,playerNum,currentWeek):
    plan=PlanSchema()
    plan.start_gameweek=squad_obj.lastUpdate+1
    plan.end_gameweek=squad_obj.lastUpdate+weeks
    plan.squads=[]
    plan.transfers=[]
    for week in range(weeks):

        future_squad=decode_future_squad(db,team[week],captain[week],subs[week],playerNum,week,currentWeek)

        future_transfer=decode_future_transfer(db,transfer_in[week],transfer_out[week],playerNum,week,currentWeek)

        plan.squads.append(future_squad)
        plan.transfers.append(future_transfer)
    return plan





