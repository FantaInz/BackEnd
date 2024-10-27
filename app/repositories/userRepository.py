from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.views.user import UserSchema,UserSchemaCreate
from app.models.user import User

async def create_user(user:UserSchemaCreate,db:AsyncSession):
    transaction=User(**user.dict())
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def get_user_by_username(username:str,db:AsyncSession):
    return await db.execute(select(User).where(User.username==username))



