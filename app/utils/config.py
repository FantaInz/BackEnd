import json
import os

from annotated_types.test_cases import cases


class Db_config:
    with open("app/resources/db_config.json",'r') as f:
        __DB_PARAMS=json.load(f)
    DB_CONFIG ="postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER",__DB_PARAMS.get("DB_USER")),
            DB_PASSWORD=os.getenv("DB_PASSWORD",__DB_PARAMS.get("DB_PASSWORD")),
            DB_HOST=os.getenv("DB_HOST",__DB_PARAMS.get("DB_HOST")),
            DB_NAME=os.getenv("DB_NAME",__DB_PARAMS.get("DB_NAME")),
        )
db_config = Db_config

class Jwt_config:
    with open("app/resources/token_config.json",'r') as f:
        __JWT_PARAMS=json.load(f)
        SECRET_KEY =os.getenv("SECRET_KEY",__JWT_PARAMS.get("SECRET_KEY"))
        ALGORITHM = os.getenv("ALGORITHM",__JWT_PARAMS.get("ALGORITHM"))
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",__JWT_PARAMS.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
jwt_config = Jwt_config


class Google_config:
    with open("app/resources/google_config.json",'r') as f:
        __GOOGLE_PARAMS=json.load(f)
        GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID",__GOOGLE_PARAMS.get("GOOGLE_CLIENT_ID"))
        GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET",__GOOGLE_PARAMS.get("GOOGLE_CLIENT_SECRET"))
        GOOGLE_REDIRECT_URI=os.getenv("GOOGLE_REDIRECT_URI",__GOOGLE_PARAMS.get("GOOGLE_REDIRECT_URI"))
google_config = Google_config

