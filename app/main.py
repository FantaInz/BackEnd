from contextlib import asynccontextmanager

from dns.rdtypes.svcbbase import ALPNParam
from fastapi import FastAPI

from app.utils.config import db_config
from app.services.database import sessionmanager
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import jwt_config
from starlette.middleware.sessions import SessionMiddleware

lifespan = None


sessionmanager.init(db_config.DB_CONFIG)
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

server = FastAPI(title="FastAPI server", lifespan=lifespan)
ALLOWED_HOSTS = ["*"]
server.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server.add_middleware(SessionMiddleware,secret_key=jwt_config.SECRET_KEY)

from app.controllers.userController import router as user_router
from app.controllers.auth.nativeAuth import router as auth_router
from app.controllers.auth.googleAuth import router as google_auth_router

server.include_router(user_router, prefix="/api", tags=["user"])
server.include_router(auth_router, prefix="/api", tags=["auth"])
server.include_router(google_auth_router, prefix="/api", tags=["google"])