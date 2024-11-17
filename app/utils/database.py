import contextlib
from typing import AsyncIterator
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self):
        self._engine: Engine | None = None
        self._sessionmaker: sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_engine(host)
        self._sessionmaker = sessionmaker(autocommit=False, bind=self._engine)

    def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    def connect(self):
        with self._engine.connect() as connection:
            yield connection

    def session(self):
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()



sessionmanager = DatabaseSessionManager()

async def get_db():
    yield sessionmanager._sessionmaker()