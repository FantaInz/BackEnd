from alembic.command import history
from app.models.player import Player
import requests,json
from app.utils.config import db_config
import asyncio
from decimal import Decimal
from rich.pretty import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.base import state_str


def get_players(URL):
    engine = create_engine(URL)
    base_url = "https://fantasy.premierleague.com/api/"
    playersUrl=base_url+"bootstrap-static/"
    response = requests.get(playersUrl)
    data = response.json()
    playersList = []
    elems = data['elements']
    for elem in elems:
        p = Player()
        p.id=int(elem['id'])
        p.name=elem['first_name']+" "+elem['second_name']
        p.position=elem['element_type']
        p.team_id=elem['team']
        p.price=int(elem['now_cost'])
        precision = Decimal('0.01')
        p.expectedPoints=[Decimal(elem['ep_this']).quantize(precision),Decimal(elem['ep_next']).quantize(precision)]
        p.availability=elem["chance_of_playing_this_round"] if elem["chance_of_playing_this_round"] is not None else 0
        historyUrl=base_url+"element-summary/"+str(p.id)+"/"
        resp=requests.get(historyUrl).json()
        points=[]
        for h in resp['history']:
            points.append(h['total_points'])
        while points.__len__()<11:
            points.insert(0,-999)
        p.points=points
        playersList.append(p)
        if len(points)!=11:
            print(p.__dict__)
    with Session(engine) as session:
         with session.begin():
              for player in playersList:
                  del player.__dict__['_sa_instance_state']
                  stmt=insert(Player).values(player.__dict__)
                  stmt=stmt.on_conflict_do_update(index_elements=["id"],set_=player.__dict__)
                  session.execute(stmt)
              session.commit()
    engine.dispose()

