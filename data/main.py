
from sqlalchemy.orm import Session
from sqlalchemy.testing.plugin.plugin_base import engines
from sqlalchemy.dialects.postgresql import insert
import os
os.chdir("..")
from sqlalchemy import create_engine, Select
from app.utils.config import db_config
from app.models.squad import Squad
##TODO rozszerzyć dla zawodnika- czy jebnie jak mu podam team_id ?


def do():
    engine = create_engine(db_config.DB_CONFIG)
    with Session(engine) as session:

        s=Squad()
        s.id=1
        s.name = "test2"
        s.lastUpdate = -1
        s.freeTransfers=69
        s.transferBudget = 1337
        s_dict=s.__dict__
        print(s_dict)
        print(s.__dict__)
        del s_dict['_sa_instance_state']
        print(s_dict)
        print(s.__dict__)
        stmt=insert(Squad).values(s.__dict__)
        stmt=stmt.on_conflict_do_update(index_elements=["id"],set_=s.__dict__)
        session.execute(stmt)
        session.commit()


do()