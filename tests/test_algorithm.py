from app.models.transfer import Transfer
from fastapi.testclient import TestClient
from app.main import server
from app.utils.database import get_db
from psycopg.postgres import types
from tests.fixtures import create_and_delete_database
from tests.utils import override_get_db
from app.models.squad import Squad,Player
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

