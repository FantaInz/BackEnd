from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from datetime import timedelta
import jwt
from typing import Annotated

from app.controllers.auth.common import Token,CREDENTIALS_EXCEPTION,create_access_token,authenticate_user
from app.utils.database import get_db
from app.repositories import userRepository
from app.utils.config import jwt_config
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])



n_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_native_user(token: Annotated[str, Depends(n_oauth2_scheme)],db: AsyncSession = Depends(get_db)):
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


@router.post("/login")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: AsyncSession = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@router.get("/me")
def read_users_me(
    current_user: Annotated[User, Depends(get_current_native_user)],
):
    current_user=current_user
    return current_user
