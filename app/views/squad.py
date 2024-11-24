from app.views.player import PlayerSchema
from pydantic import BaseModel
from app.views.transfer import TransferSchema

class SquadSchema(BaseModel):
    id:int|None =None
    name:str|None=None
    transferBudget:int|None=None
    freeTransfers:int|None=None
    lastUpdate:int|None=None
    players:list[PlayerSchema]|None=None
    transfers:list[TransferSchema]|None=None

    @classmethod
    def from_model(cls,model)->"SquadSchema":
        squadSchema=SquadSchema()
        squadSchema.id=model.id
        squadSchema.name=model.name
        squadSchema.transferBudget=model.transferBudget
        squadSchema.freeTransfers=model.freeTransfers
        squadSchema.lastUpdate=model.lastUpdate
        squadSchema.players=[PlayerSchema.from_model(player) for player in model.players]
        squadSchema.transfers=[TransferSchema.from_model(transfer) for transfer in model.transfers]
        return squadSchema

