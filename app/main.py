from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.utils.config import db_config
from app.utils.database import sessionmanager
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.auth.common import get_current_user
from fastapi.params import Depends



lifespan = None


sessionmanager.init(db_config.DB_CONFIG)

def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        sessionmanager.close()

server = FastAPI(title="FastAPI server", lifespan=lifespan)
ALLOWED_HOSTS = ["*"]
server.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.controllers.userController import router as user_router
from app.controllers.auth.nativeAuth import router as auth_router
from app.controllers.auth.googleAuth import router as google_auth_router
from app.controllers.squadController import router as squad_router
server.include_router(user_router, prefix="/api", tags=["user"])
server.include_router(auth_router, prefix="/api", tags=["auth"])
server.include_router(google_auth_router, prefix="/api", tags=["google"])
server.include_router(squad_router, prefix="/api", tags=["squad"])
@server.get("/user")
def get_user(user=Depends(get_current_user)):
    return user