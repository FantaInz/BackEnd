from pydantic import BaseModel
from app.views.player import PlayerSchema
from decimal import Decimal
from app.views.futureSquad import FutureSquadSchema
from app.views.futureTransfer import FutureTransferSchema



class PlanSchema(BaseModel):
    id : int|None =None
    user_id: int|None =None
    squad_id: int|None =None
    name: str|None =None
    start_gameweek: int|None =None
    end_gameweek: int|None =None
    squads:list[FutureSquadSchema]|None =None
    transfers:list[FutureTransferSchema]|None =None
    @classmethod
    def from_model(cls,model):
        return cls(
            id=model.id,
            user_id=model.user_id,
            squad_id=model.squad_id,
            name=model.name,
            start_gameweek=model.start_gameweek,
            end_gameweek=model.end_gameweek,
            squads=[FutureSquadSchema.from_model(squad) for squad in model.futureSquads],
            transfers=[FutureTransferSchema.from_model(transfer) for transfer in model.futureTransfers]
        )

class PlanSchemaList(BaseModel):
    id:int | None =None
    user_id:int | None =None
    name:str | None =None
    start_gameweek:int | None =None
    end_gameweek:int | None =None
    @classmethod
    def from_model(cls,model):
        return cls(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            start_gameweek=model.start_gameweek,
            end_gameweek=model.end_gameweek
        )



