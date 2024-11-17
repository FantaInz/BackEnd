from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tests.fixtures import TEST_URL

def override_get_db():
    test_engine = create_engine(TEST_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()