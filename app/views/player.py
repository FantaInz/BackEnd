from pydantic import BaseModel


class playerSchema(BaseModel):
    id: int
    name: str
    age: int