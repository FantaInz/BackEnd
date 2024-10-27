from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.services.database import get_db
from app.repositories import userRepository
from app.views.user import UserSchema,UserSchemaCreate

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserSchema)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await userRepository.create_user(user, db)
    except IntegrityError:
        raise HTTPException(status_code=409,detail="User with this username or email already exists")
    if user.id is None:
        raise HTTPException(status_code=500,detail="couldn't register user")
    return user