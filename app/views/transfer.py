from pydantic import BaseModel
from app.models.transfer import Transfer
from app.views.player import PlayerSchema

class TransferSchema(BaseModel):
    id: int|None = None
    playerIn: PlayerSchema|None = None
    priceIn: int|None = None
    playerOut: PlayerSchema|None = None
    priceOut: int|None = None
    @classmethod
    def from_model(cls, model: "Transfer") -> "TransferSchema":
        return TransferSchema(
            id=model.id,
            playerIn=PlayerSchema.from_model(model.playerIn),
            playerOut=PlayerSchema.from_model(model.playerOut),
            priceIn=model.inPlayerPrice,
            priceOut=model.outPlayerPrice,
        )