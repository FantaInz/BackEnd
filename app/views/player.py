import decimal
from app.views.team import TeamSchema
from pydantic import BaseModel,Field
from decimal import Decimal
from app.models.player import Player
position_dict={
    1:"Goalkeeper",
    2:"Defender",
    3:"Midfielder",
    4:"Forward"
}
class PlayerSchema(BaseModel):
    id: int|None =None
    name: str|None =None
    position: str|None =None
    price : int|None =None
    team :TeamSchema|None =None
    points: list[int]|None =None
    expectedPoints: list[Decimal]|None =None
    availability: int|None =None
    @classmethod
    def from_model(cls,model:Player)->"PlayerSchema":
        return PlayerSchema(
            id=model.id,
            name=model.name,
            position=position_dict[model.position],
            price=model.price,
            points=model.points,
            expectedPoints=model.expectedPoints,
            availability=model.availability,
            team=TeamSchema.from_model(model.team)
        )


class PlayerSearch(BaseModel):
    teams: list[int]|None =None
    positions: list[int]|None =None
    name: str|None =None
    minPrice: int|None =None
    maxPrice: int|None =None
    pageSize: int=Field(10,ge=1)
    pageNumber: int=Field(0,ge=0)