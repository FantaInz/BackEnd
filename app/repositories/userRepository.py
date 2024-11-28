from sqlalchemy.orm import Session
from sqlalchemy import select
from app.views.user import UserSchemaCreate
from app.models.user import User
from app.utils.passwords import get_password_hash

def create_user(user:UserSchemaCreate,db:Session):
    if user.password is not None:
        user.password=get_password_hash(user.password)
    transaction=User(**user.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_user_by_username(username:str,db:Session):
    statement = select(User).where(User.username == username)
    result =db.execute(statement)
    user:User =result.scalar()
    return user



