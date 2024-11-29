
from app.models.player import Player
import requests

from decimal import Decimal


from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert



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
        p.availability=elem["chance_of_playing_this_round"] if elem["chance_of_playing_this_round"] is not None else 0
        historyUrl=base_url+"element-summary/"+str(p.id)+"/"
        resp=requests.get(historyUrl).json()
        limit=int(resp["fixtures"][0]["event"])-1
        points=[]
        for h in resp['history']:
            points.append(h['total_points'])
        while points.__len__()<limit:
            points.insert(0,-999)
        p.points=points
        playersList.append(p)
        p.expectedPoints=[0 for i in range(limit+4)]
    with Session(engine) as session:
         with session.begin():
              for player in playersList:
                  player_dir=player.__dict__
                  del player_dir['_sa_instance_state']
                  stmt=insert(Player).values(player.__dict__)
                  del player_dir["expectedPoints"]
                  stmt=stmt.on_conflict_do_update(index_elements=["id"],set_=player_dir)
                  session.execute(stmt)
              session.commit()
    engine.dispose()

