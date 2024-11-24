from pydantic import BaseModel
from app.views.player import PlayerSchema

class FutureTransferSchema(BaseModel):
    id:int|None =None
    plan_id:int|None =None
    gameweek:int|None =None
    transfer_in:list[PlayerSchema]|None =None
    transfer_out:list[PlayerSchema]|None =None
    @classmethod
    def from_model(cls,model):
        return cls(
            id=model.id,
            plan_id=model.plan_id,
            gameweek=model.gameweek,
            transfer_in=[PlayerSchema.from_model(player) for player in model.players_in],
            transfer_out=[PlayerSchema.from_model(player) for player in model.players_out]
        )
