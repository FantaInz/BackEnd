
from pydantic import BaseModel
from fastapi import HTTPException,status
from datetime import datetime, timedelta, timezone
import jwt
from app.repositories import userRepository
from app.utils.config import jwt_config
from app.utils.passwords import verify_password
class Token(BaseModel):
    access_token: str
    token_type: str

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

def authenticate_user(db, username: str, password: str):
    user =  userRepository.get_user_by_username(username,db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_config.SECRET_KEY, algorithm=jwt_config.ALGORITHM)
    return encoded_jwt


from app.controllers.auth.nativeAuth import get_current_native_user
from app.controllers.auth.googleAuth import get_current_google_user
from app.models.user import User
from typing import Annotated
from fastapi.params import Depends
from fastapi import HTTPException,status


def get_current_user(google_user: Annotated[User, Depends(get_current_google_user)],
                           current_user: Annotated[User, Depends(get_current_native_user)]):
    if not(google_user or current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="login required")
    if google_user:
        return google_user
    return current_user




