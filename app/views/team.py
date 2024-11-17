from pydantic import BaseModel


class TeamSchema(BaseModel):
    id:int|None =None
    name:str|None=None
    @classmethod
    def from_model(cls,model)->"TeamSchema":
        return TeamSchema(
            id=model.id,
            name=model.name
        )