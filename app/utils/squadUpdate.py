from app.models.transfer import Transfer
import requests


baseUrl="https://fantasy.premierleague.com/api/"
def get_transfers_info(squad_id,gameWeek):
    infoList=[]
    for i in range(1,gameWeek):
        infoElem=dict()
        response=requests.get(baseUrl+"entry/"+str(squad_id)+"/event/"+str(i)+"/picks/").json()
        infoElem["active_chip"]=response["active_chip"]
        infoElem["event_transfers"]=response["entry_history"]["event_transfers"]
        infoElem["event_transfers_cost"]=response["entry_history"]["event_transfers_cost"]
        infoList.append(infoElem)
    return infoList

def calculate_free_transfers(infoList):
    freeTransfers=0
    for info in infoList:
        freeTransfers+=1
        if info["active_chip"]=="wildcard":
            continue
        freeTransfers=freeTransfers-int(info["event_transfers"])+(int(info["event_transfers_cost"])/4)
    if freeTransfers>5:
        freeTransfers=5
    return freeTransfers

def create_transfer_from_json(json):
    transfer=Transfer()
    transfer.gameWeek=int(json["event"])
    transfer.inPlayerId=json["element_in"]
    transfer.outPlayerId=json["element_out"]
    transfer.inPlayerPrice=json["element_in_cost"]
    transfer.outPlayerPrice=json["element_out_cost"]
    return transfer

def update_transfers(transfersResponse,lastUpdate):
    transfers=[]
    for transferResponse in transfersResponse:
        transfer_time = int(transferResponse["event"])
        if transfer_time > lastUpdate:
            transfer = create_transfer_from_json(transferResponse)
            transfers.append(transfer)
    return transfers
