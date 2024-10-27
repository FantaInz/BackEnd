from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.views.user import UserSchemaCreate
from app.models.user import User
from app.controllers.auth.nativeAuth import get_password_hash

async def create_user(user:UserSchemaCreate,db:AsyncSession):
    user.password=get_password_hash(user.password)
    transaction=User(**user.dict())
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def get_user_by_username(username:str,db:AsyncSession):
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    user:User =result.scalar()
    print(user)
    return user



