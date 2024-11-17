import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.session import close_all_sessions
from app.main import server
from sqlalchemy import create_engine
from app.utils.database import get_db, Base
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.orm import sessionmaker
TEST_URL="postgresql://postgres:postgres@localhost:5433/TEST"
fixture_used = False


@pytest.fixture(scope="session", autouse=True)
def create_and_delete_database():
    global fixture_used

    if fixture_used:
        yield
        return

    if database_exists(TEST_URL):
        drop_database(TEST_URL)

    create_database(TEST_URL)

    test_engine = create_engine(TEST_URL)

    Base.metadata.create_all(bind=test_engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    fixture_used = True
    yield SessionLocal()

    close_all_sessions()

    drop_database(TEST_URL)
@pytest.fixture(scope="session")
def override_get_db():
    test_engine = create_engine(TEST_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture(scope="session")
def test_client(override_get_db):
    with TestClient(server) as client:
        server.dependency_overrides[get_db] = override_get_db
        yield client
        close_all_sessions()
        override_get_db.close()



