
from app.models.team import Team
import requests,json
from app.utils.config import db_config
import asyncio
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
def get_teams(URL):
    engine = create_engine(URL)
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    teamsList = []
    teams = data['teams']
    for team in teams:
        t = Team()
        t.name = team['name']
        t.id = team['id']
        teamsList.append(t)
    with Session(engine) as session:
         with session.begin():
            for team in teamsList:
                del team.__dict__['_sa_instance_state']
                stmt=insert(Team).values(team.__dict__)
                stmt=stmt.on_conflict_do_update(index_elements=["id"],set_=team.__dict__)
                print(team.__dict__)
                session.execute(stmt)
            session.commit()
    engine.dispose()