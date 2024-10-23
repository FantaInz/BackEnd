from dataclasses import dataclass
from typing import Any
import os
import json


class DB_Config:
    with open("app/resources/db_config.json",'r') as f:
        __DB_PARAMS=json.load(f)
    DB_CONFIG ="postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=__DB_PARAMS["DB_USER"],
            DB_PASSWORD=__DB_PARAMS["DB_PASSWORD"],
            DB_HOST=__DB_PARAMS["DB_HOST"],
            DB_NAME=__DB_PARAMS["DB_NAME"],
        )
db_config = DB_Config()