from pydantic import BaseModel
from app.models.transfer import Transfer
from app.views.player import PlayerSchema

class TransferSchema(BaseModel):
    id: int|None = None
    playerIn: int|None = None
    team_id: int|None = None
    priceIn: int|None = None
    @classmethod
    def from_model(cls, model: "Transfer") -> "TransferSchema":
        return TransferSchema(
            id=model.id,
            player_id=model.player_id,
            team_id=model.team_id,
            price=model.price
        )