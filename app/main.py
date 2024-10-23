from fastapi import FastAPI
from app.utils.config import db_config
app = FastAPI()
print(db_config.DB_CONFIG)
@app.get("/")
async def root():
    return {"message": "Hello World"}