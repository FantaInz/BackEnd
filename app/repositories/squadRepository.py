from app.models.transfer import Transfer
from sqlalchemy.orm import Session
from sqlalchemy import select
import logging
import requests
from app.models.squad import Squad,Player
from sqlalchemy.orm import defer

baseUrl="https://fantasy.premierleague.com/api/"
def create_squad(squad_id,db: Session):
    squad = Squad()
    squad.players=[]
    squad.id=squad_id
    managerResponse=requests.get(baseUrl+"entry/"+str(squad_id)+"/").json()
    squad.name=managerResponse["name"]
    statusResponse = requests.get(baseUrl+"event-status/").json()
    gameweek=int(statusResponse["status"][-1]["event"])
    squad.lastUpdate=gameweek
    squadResponse=requests.get(baseUrl+"entry/"+str(squad_id)+"/event/"+str(gameweek)+"/picks/").json()
    squad.transferBudget=squadResponse["entry_history"]["bank"]
    members=squadResponse["picks"]
    for member in members:
        player=db.execute(select(Player).filter(Player.id==member["element"]))
        player=player.scalars().first()
        squad.players.append(player)
    squad.freeTransfers=1
    squad.transfers=[]
    transfersResponse=requests.get(baseUrl+"entry/"+str(squad_id)+"/transfers/").json()
    for transferResponse in transfersResponse:
        transfer=Transfer()
        transfer.squad_id=squad_id
        transfer.gameWeek=int(transferResponse["event"])
        transfer.inPlayerId=transferResponse["element_in"]
        transfer.outPlayerId=transferResponse["element_out"]
        transfer.inPlayerPrice=transferResponse["element_in_cost"]
        transfer.outPlayerPrice=transferResponse["element_out_cost"]
        squad.transfers.append(transfer)
    db.add(squad)
    db.commit()
    db.refresh(squad)
    return squad

def update_squad(squad,db: Session):
    squad_id=squad.id
    managerResponse = requests.get(baseUrl + "entry/" + str(squad_id) + "/").json()
    squad.name = managerResponse["name"]
    statusResponse = requests.get(baseUrl + "event-status/").json()
    gameweek = int(statusResponse["status"][-1]["event"])
    squadResponse = requests.get(baseUrl + "entry/" + str(squad_id) + "/event/" + str(gameweek) + "/picks/").json()
    squad.transferBudget = squadResponse["entry_history"]["bank"]
    members = squadResponse["picks"]
    squad.players=[]
    for member in members:
        player = db.execute(select(Player).filter(Player.id == member["element"]))
        player = player.scalars().first()
        squad.players.append(player)
    transfersResponse = requests.get(baseUrl + "entry/" + str(squad_id) + "/transfers/").json()
    for transferResponse in transfersResponse:
        transfer_time=int(transferResponse["event"])
        if transfer_time>squad.lastUpdate:
            transfer = Transfer()
            transfer.squad_id = squad_id
            transfer.gameWeek = int(transferResponse["event"])
            transfer.inPlayerId = transferResponse["element_in"]
            transfer.outPlayerId = transferResponse["element_out"]
            transfer.inPlayerPrice = transferResponse["element_in_cost"]
            transfer.outPlayerPrice = transferResponse["element_out_cost"]
            squad.transfers.append(transfer)
    squad.lastUpdate=gameweek
    db.commit()
    db.refresh(squad)
    return squad


def update_or_create_squad(squad_id, db: Session):
    result = db.execute(select(Squad).filter(Squad.id == squad_id))
    squad = result.scalars().first()
    if squad is None:
        return create_squad(squad_id,db)
    else:
        return update_squad(squad,db)

