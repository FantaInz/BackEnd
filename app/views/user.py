from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    username: str|None = None
    email: str | None = None
    password: str | None = None
    team_id: int | None = None

class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: int|None = None

    class Config:
        orm_mode = True


