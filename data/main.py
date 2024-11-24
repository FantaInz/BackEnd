
from sqlalchemy.orm import Session
from sqlalchemy.testing.plugin.plugin_base import engines
from sqlalchemy.dialects.postgresql import insert
import os
os.chdir("..")
from sqlalchemy import create_engine, Select
from app.utils.config import db_config
from app.models.squad import Squad
from data.insert_teams import get_teams
from data.insert_players import get_players


get_teams(db_config.DB_CONFIG)
get_players(db_config.DB_CONFIG)