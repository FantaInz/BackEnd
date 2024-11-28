from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.utils.passwords import get_password_hash
from app.models.team import Team

def get_team_by_id(team_id: int, db: Session):
    result = db.execute(select(Team).filter(Team.id == team_id))
    return result.scalars().first()

def get_teams( db: Session):
    result = db.execute(select(Team))
    return result.scalars().all()

