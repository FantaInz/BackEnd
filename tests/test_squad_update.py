from app.models.transfer import Transfer
from fastapi.testclient import TestClient
from app.main import server
from app.utils.database import get_db
from psycopg.postgres import types
from tests.fixtures import create_and_delete_database
from tests.utils import override_get_db
import json
client = TestClient(server)
server.dependency_overrides[get_db] = override_get_db
from data.insert_teams import get_teams
from data.insert_players import get_players
from tests.conftest import TEST_URL
from app.utils.squadUpdate import create_transfer_from_json, update_transfers,calculate_free_transfers


def test_transfer_from_json():
   data="""
    {
    "element_in": 328,
    "element_in_cost": 127,
    "element_out": 54,
    "element_out_cost": 52,
    "entry": 2100,
    "event": 11,
    "time": "2024-11-03T01:24:13.065188Z"
    }
   """
   jsonData=json.loads(data)
   transfer=create_transfer_from_json(jsonData)
   assert transfer.gameWeek==11
   assert transfer.inPlayerId==328
   assert transfer.outPlayerId==54
   assert transfer.inPlayerPrice==127
   assert transfer.outPlayerPrice==52

def test_transfers_from_response_already_exists():
    response="""
    [
     {
       "element_in": 328,
       "element_in_cost": 127,
       "element_out": 54,
       "element_out_cost": 52,
       "entry": 2100,
       "event": 11,
       "time": "2024-11-03T01:24:13.065188Z"
     },
     {
       "element_in": 566,
       "element_in_cost": 55,
       "element_out": 351,
       "element_out_cost": 153,
       "entry": 2100,
       "event": 11,
       "time": "2024-11-03T01:24:13.060697Z"
     },
     {
       "element_in": 182,
       "element_in_cost": 108,
       "element_out": 17,
       "element_out_cost": 100,
       "entry": 2100,
       "event": 9,
       "time": "2024-10-19T15:19:29.716150Z"
     }
    ]
    """
    responseData=json.loads(response)
    transfers=update_transfers(responseData,10)
    assert len(transfers)==2


def test_transfers_from_response_new_squad():
   response = """
    [
     {
       "element_in": 328,
       "element_in_cost": 127,
       "element_out": 54,
       "element_out_cost": 52,
       "entry": 2100,
       "event": 11,
       "time": "2024-11-03T01:24:13.065188Z"
     },
     {
       "element_in": 566,
       "element_in_cost": 55,
       "element_out": 351,
       "element_out_cost": 153,
       "entry": 2100,
       "event": 11,
       "time": "2024-11-03T01:24:13.060697Z"
     },
     {
       "element_in": 182,
       "element_in_cost": 108,
       "element_out": 17,
       "element_out_cost": 100,
       "entry": 2100,
       "event": 9,
       "time": "2024-10-19T15:19:29.716150Z"
     }
    ]
    """

   responseData = json.loads(response)
   transfers = update_transfers(responseData, 0)
   assert len(transfers) == 3

def test_calculate_free_transfers():
    infoList=[
        {
            "active_chip":None,
            "event_transfers":2,
            "event_transfers_cost":4
        },
        {
            "active_chip":None,
            "event_transfers":1,
            "event_transfers_cost":0
        },
        {
            "active_chip":"wildcard",
            "event_transfers":2,
            "event_transfers_cost":0
        }
    ]
    freeTransfers=calculate_free_transfers(infoList)
    assert freeTransfers==1

def test_calculate_free_transfers_max():
    infoList=[
        {
            "active_chip":None,
            "event_transfers":0,
            "event_transfers_cost":0
        },
        {
            "active_chip":None,
            "event_transfers":0,
            "event_transfers_cost":0
        },
        {
            "active_chip":None,
            "event_transfers":0,
            "event_transfers_cost":0
        },
        {
            "active_chip":None,
            "event_transfers":0,
            "event_transfers_cost":0
        },
        {
            "active_chip":None,
            "event_transfers":0,
            "event_transfers_cost":0
        },
        {
            "active_chip":None,
            "event_transfers":0,
            "event_transfers_cost":0
        }
    ]
    freeTransfers=calculate_free_transfers(infoList)
    assert infoList.__len__()>5
    assert freeTransfers==5

def a_test_squad_update():
    get_teams(TEST_URL)
    get_players(TEST_URL)
    response = client.get(f"/api/squad/update/1")
    assert response.status_code == 200
    assert response.json()["id"]==1

def test_squad_update_bad_request():
    response = client.get(f"/api/squad/update/-11")
    assert response.status_code == 404
    assert response.json()["detail"]=="Manager not found"