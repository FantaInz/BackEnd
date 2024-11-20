from fastapi.testclient import TestClient
from app.main import server
from app.utils.database import get_db
from tests.fixtures import create_and_delete_database
from tests.utils import override_get_db
import json
client = TestClient(server)
server.dependency_overrides[get_db] = override_get_db
from data.insert_teams import get_teams
from data.insert_players import get_players
from tests.conftest import TEST_URL

def  test_create_user():
    response =  client.post(
        "/api/user/register",
        json={"username":"test","password":"test","email":"test@example.com"}
        )
    assert response.status_code == 200
    assert response.json()["username"] == "test"
    assert response.json()["email"] == "test@example.com"
    assert response.json()["squad_id"] == None
    assert response.json()["id"] is not None



def test_user_already_exists():
     rsp=client.post(
        "/api/user/register",
        json={"username":"test","password":"test","email":"test@example.com"}
        )
     assert rsp.status_code == 200

     response=client.post(
         "/api/user/register",
         json={"username": "test", "password": "test", "email": "test@example.com"}
     )
     assert response.status_code == 409
     assert response.json()["detail"] == "User with this username or email already exists"

def test_user_login():
    rsp1 = client.post(
        "/api/user/register",
        json={"username": "test", "password": "test", "email": "test@example.com"}
    )
    rsp2 = client.post(
        "/api/auth/login",
        data={"username": "test", "password": "test"}
    )
    assert rsp1.status_code == 200
    assert rsp2.status_code == 200
    assert rsp2.json()["access_token"] is not None
    assert rsp2.json()["token_type"] == "bearer"

def test_bad_credencials():
    rsp1 = client.post(
        "/api/user/register",
        json={"username": "test", "password": "test", "email": "test@example.com"}
    )
    rsp2 = client.post(
        "/api/auth/login",
        data={"username": "test", "password": "nottest"}
    )
    rsp3 = client.post(
        "/api/auth/login",
        data={"username": "nottest", "password": "test"}
    )

    assert rsp1.status_code == 200
    assert rsp2.status_code == 401
    assert rsp2.json()["detail"] == "Incorrect username or password"
    assert rsp3.status_code == 401
    assert rsp3.json()["detail"] == "Incorrect username or password"

def test_no_user_login():
    rsp = client.post(
        "/api/auth/login",
        data={"username": "notExisiting", "password": "notExisiting"}
    )
    assert rsp.status_code == 401
    assert rsp.json()["detail"] == "Incorrect username or password"

def test_authenticate_user():
    rsp1 = client.post(
        "/api/user/register",
        json={"username": "test", "password": "test", "email": "test@example.com"}
    )
    rsp2 = client.post(
        "/api/auth/login",
        data={"username": "test", "password": "test"}
    )
    rsp3 = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {rsp2.json()['access_token']}"}
    )
    assert rsp1.status_code == 200
    assert rsp2.status_code == 200
    assert rsp3.status_code == 200
    assert rsp3.json()["username"] == "test"
    assert rsp3.json()["email"] == "test@example.com"
    assert rsp3.json()["squad_id"] == None
    assert rsp3.json()["id"] is not None
    assert rsp3.json()["password"] is not None

