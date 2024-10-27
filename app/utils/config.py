import json

from annotated_types.test_cases import cases


class Db_config:
    with open("app/resources/db_config.json",'r') as f:
        __DB_PARAMS=json.load(f)
    DB_CONFIG ="postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=__DB_PARAMS["DB_USER"],
            DB_PASSWORD=__DB_PARAMS["DB_PASSWORD"],
            DB_HOST=__DB_PARAMS["DB_HOST"],
            DB_NAME=__DB_PARAMS["DB_NAME"],
        )
db_config = Db_config

class Jwt_config:
    with open("app/resources/token_config.json",'r') as f:
        __JWT_PARAMS=json.load(f)
        SECRET_KEY =__JWT_PARAMS["SECRET_KEY"]
        ALGORITHM = __JWT_PARAMS["ALGORITHM"]
        ACCESS_TOKEN_EXPIRE_MINUTES = __JWT_PARAMS["ACCESS_TOKEN_EXPIRE_MINUTES"]
jwt_config = Jwt_config


class Google_config:
    with open("app/resources/google_config.json",'r') as f:
        __GOOGLE_PARAMS=json.load(f)
        GOOGLE_CLIENT_ID=__GOOGLE_PARAMS["GOOGLE_CLIENT_ID"]
        GOOGLE_CLIENT_SECRET=__GOOGLE_PARAMS["GOOGLE_CLIENT_SECRET"]
        GOOGLE_REDIRECT_URI=__GOOGLE_PARAMS["GOOGLE_REDIRECT_URI"]
google_config = Google_config

