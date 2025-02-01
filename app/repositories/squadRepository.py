from app.models.transfer import Transfer
from sqlalchemy.orm import Session
from sqlalchemy import select
import requests
from app.models.squad import Squad,Player
from fastapi import HTTPException
from app.utils.squadUpdate import get_transfers_info,calculate_free_transfers, update_transfers
from app.models.user import User
baseUrl="https://fantasy.premierleague.com/api/"


def update_or_create_squad(squad_id,user:User, db: Session):
    if user.squad_id is not None and user.squad_id!=squad_id:
        raise HTTPException(status_code=403, detail="User does not have access to this squad")
    result = db.execute(select(Squad).filter(Squad.id == squad_id))
    squad = result.scalars().first()
    if squad is None:
        doesnt_exist=True
        squad=Squad()
        squad.id = squad_id
        squad.transfers=[]
    else:
        doesnt_exist=False
    try:
        managerResponse = requests.get(baseUrl + "entry/" + str(squad_id) + "/").json()
        squad.name = managerResponse["name"]
    except:
        raise HTTPException(status_code=404, detail="Manager not found")
    gameweek = int(managerResponse["current_event"])
    squadResponse = requests.get(baseUrl + "entry/" + str(squad_id) + "/event/" + str(gameweek) + "/picks/").json()
    squad.transferBudget = squadResponse["entry_history"]["bank"]


    members = squadResponse["picks"]
    squad.players = []
    for member in members:
        if member["position"]!= 16:
            player = db.execute(select(Player).filter(Player.id == member["element"]))
            player = player.scalars().first()
            squad.players.append(player)


    transfersResponse = requests.get(baseUrl + "entry/" + str(squad_id) + "/transfers/").json()
    if doesnt_exist:
        last_update=0
    else:
        last_update = squad.lastUpdate
    transfers=update_transfers(transfersResponse,last_update)
    squad.transfers+=transfers
    squad.lastUpdate = gameweek

    infoList=get_transfers_info(squad_id,gameweek)
    squad.freeTransfers=calculate_free_transfers(infoList)
    user.squad_id=squad.id
    if doesnt_exist:
        db.add(squad)
    db.commit()
    db.refresh(user)
    db.refresh(squad)
    return squad




