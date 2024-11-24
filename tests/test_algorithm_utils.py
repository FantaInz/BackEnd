from app.models.transfer import Transfer
from fastapi.testclient import TestClient
from app.main import server
from app.utils.database import get_db
from psycopg.postgres import types
from tests.fixtures import create_and_delete_database
from tests.utils import override_get_db
from app.services.algorithm.utils import encode_squad,get_decision_array, create_players_dataframe
from app.models.squad import Squad,Player
import pandas as pd
import numpy as np
from decimal import Decimal
def test_player_to_dict():
    player=Player(id=1,name="Jhon Doe",position=1,price=100,expectedPoints=[Decimal(2.1),Decimal(2.3),Decimal(3.4)]
                         ,points=[1,2,3],availability=50,team_id=1)
    playerDict=player.to_dict()
    assert playerDict["id"]==1
    assert playerDict["name"]=="Jhon Doe"
    assert playerDict["position"]==1
    assert playerDict["price"]==100
    assert playerDict["expectedPoints"]==[Decimal(2.1),Decimal(2.3),Decimal(3.4)]
    assert playerDict["availability"]==50

def test_squad_to_df():
    squad=Squad()
    squad.transfers=[]
    players=[]
    for i in range(1,5):
        player=Player(id=i,name=f"Jhon Doe{i}",position=1,price=100,expectedPoints=[Decimal(2.1),Decimal(2.3),Decimal(3.4)]
                         ,points=[1,2,3],availability=50,team_id=1)
        players.append(player)

    transfer_1=Transfer(inPlayerId=1,outPlayerId=6,inPlayerPrice=60,outPlayerPrice=100,gameWeek=1)
    transfer_2 = Transfer(inPlayerId=1, outPlayerId=6, inPlayerPrice=80, outPlayerPrice=100, gameWeek=2)
    transfer_3=Transfer(inPlayerId=3,outPlayerId=7,inPlayerPrice=120,outPlayerPrice=100,gameWeek=1)
    squad.transfers.append(transfer_1)
    squad.transfers.append(transfer_2)
    squad.transfers.append(transfer_3)
    df=create_players_dataframe(players,squad)
    print(df.iloc[0])
    assert df.iloc[0].sell_price==90
    assert df.iloc[2].sell_price==100
    assert df.shape[0]==4
    print(df.columns)
    assert "price" not in df.columns

def test_team_encoding():
    squad=Squad()
    for i in range(1,5):
        player=Player(id=2*i,name=f"Jhon Doe{i}",position=1,price=100,expectedPoints=[Decimal(2.1),Decimal(2.3),Decimal(3.4)]
                         ,points=[1,2,3],availability=50,team_id=1)
        squad.players.append(player)
    arr=encode_squad(9,squad)
    for i in range(9):
        if i%2==1:
            assert arr[i]==1
        else:
            assert arr[i]==0
    assert sum(arr)==4