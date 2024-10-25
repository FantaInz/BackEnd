from sqlalchemy.ext.asyncio import AsyncSession

from app.views.user import UserSchema,UserSchemaCreate
from app.models.user import User

async def create_user(user:UserSchemaCreate,db:AsyncSession):
    transaction=User(**user.dict())
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction



