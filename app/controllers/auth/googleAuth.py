from app.utils.database import get_db
from app.views.user import UserSchemaCreate
from fastapi import APIRouter,HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from datetime import timedelta
import requests
from app.controllers.auth.common import CREDENTIALS_EXCEPTION,Token,create_access_token
from app.repositories import userRepository
from app.utils.config import google_config,jwt_config
import jwt
from jwt.exceptions import InvalidTokenError


GOOGLE_CLIENT_ID = google_config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = google_config.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = google_config.GOOGLE_REDIRECT_URI


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/google/token')


SECRET_KEY = jwt_config.SECRET_KEY

def get_current_google_user(token: Annotated[str, Depends(oauth2_scheme)],db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION

    except InvalidTokenError:
        raise CREDENTIALS_EXCEPTION
    user = userRepository.get_user_by_username(username,db)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


def create_user_if_not_exists(userdata,db):
    user = userRepository.get_user_by_username(userdata['name'],db)
    if user is None:
        try:
            raw_user=UserSchemaCreate(username=userdata["name"],email=userdata["email"],team_id=0)
            user = userRepository.create_user(raw_user,db)
        except IntegrityError:
            raise HTTPException(status_code=409,detail="Username or email already exists")

    return user

router = APIRouter(prefix="/google",tags=["google"])
@router.get("/login")
def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/auth")
def auth_google(code: str,db:AsyncSession=Depends(get_db))->Token:
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    google_access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {google_access_token}"})
    user=create_user_if_not_exists(user_info.json(),db)
    access_token_expires = timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token,token_type="bearer")

@router.get("/me")
async def get_user(current_user=Depends(get_current_google_user)):
    current_user = current_user
    return current_user