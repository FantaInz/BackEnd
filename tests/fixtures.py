import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.session import close_all_sessions
from app.main import server
from sqlalchemy.sql import text as sa_text
from sqlalchemy import create_engine
from app.utils.database import get_db, Base
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.orm import sessionmaker
from data.insert_teams import get_teams
from data.insert_players import get_players

TEST_URL="postgresql://postgres:postgres@localhost:5433/TEST"
fixture_used = False


@pytest.fixture(scope="session", autouse=True)
def create_and_delete_database():
    global fixture_used

    if database_exists(TEST_URL):
        drop_database(TEST_URL)

    create_database(TEST_URL)

    test_engine = create_engine(TEST_URL)

    Base.metadata.create_all(bind=test_engine)
    #get_teams(TEST_URL)
    #get_players(TEST_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    yield

    close_all_sessions()
@pytest.fixture(scope="function", autouse=False)
def drop_users():
    engine = create_engine(TEST_URL)
    with engine.connect() as conn:
        conn.execute(sa_text("DELETE FROM users"))
        conn.commit()