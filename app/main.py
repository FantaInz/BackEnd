from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.utils.config import db_config
from app.services.database import sessionmanager

lifespan = None


sessionmanager.init(db_config.DB_CONFIG)
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

server = FastAPI(title="FastAPI server", lifespan=lifespan)

from app.controllers.userController import router as user_router
from app.controllers.authController import router as auth_router

server.include_router(user_router, prefix="/api", tags=["user"])
server.include_router(auth_router, prefix="/api", tags=["auth"])