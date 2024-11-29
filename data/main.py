from app.utils.config import db_config
from data.insert_teams import get_teams
from data.insert_players import get_players


get_teams(db_config.DB_CONFIG)
get_players(db_config.DB_CONFIG)